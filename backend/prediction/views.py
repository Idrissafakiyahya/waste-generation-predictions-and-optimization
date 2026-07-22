import csv
import json
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Shehia, Bin, WasteReport, SavedPredictionBatch, CollectionRecord
from .optimization import build_optimization_schedule, _map_prediction_to_priority

# Lazy-load model utilities to avoid importing heavy packages at module import time
MODEL_PATH = Path(__file__).resolve().parent.parent / "waste_model.pkl"
MODEL_PIPELINE = None
MODEL_PREDICT_FUNC = None


@csrf_exempt
def predict(request):
    global MODEL_PIPELINE, MODEL_PREDICT_FUNC
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    # Load pipeline on first request (avoids pandas import during Django startup)
    if MODEL_PIPELINE is None:
        try:
            from .model_utils import load_pipeline, predict_waste_level

            MODEL_PIPELINE = load_pipeline(MODEL_PATH)
            MODEL_PREDICT_FUNC = predict_waste_level
        except Exception as exc:
            return JsonResponse({"error": "Model not loaded.", "details": str(exc)}, status=500)

    try:
        data = json.loads(request.body.decode("utf-8"))
        timestamp = data["Timestamp"]
        shehia = data["Shehia"]
        bin_name = data["Bin"]
    except Exception as exc:
        return JsonResponse({"error": "Invalid input data.", "details": str(exc)}, status=400)

    result = MODEL_PREDICT_FUNC(MODEL_PIPELINE, timestamp, shehia, bin_name)
    return JsonResponse(result)


# ============================================
# COMMUNITY WASTE REPORTING API ENDPOINTS
# ============================================

@csrf_exempt
@require_http_methods(["GET"])
def get_shehias(request):
    """Get list of all Shehias"""
    try:
        shehias = Shehia.objects.all().values('id', 'name', 'description')
        return JsonResponse({'success': True, 'data': list(shehias)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_bins(request):
    """Get list of bins for a specific Shehia"""
    try:
        shehia_id = request.GET.get('shehia_id')
        if not shehia_id:
            return JsonResponse({'success': False, 'error': 'shehia_id required'}, status=400)
        
        bins = Bin.objects.filter(shehia_id=shehia_id).values('id', 'name', 'location', 'bin_type')
        return JsonResponse({'success': True, 'data': list(bins)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_waste_report(request):
    """Submit a waste report"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        # Validate required fields
        required_fields = ['shehia_id', 'bin_id', 'timestamp']
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {'success': False, 'error': f'Missing required field: {field}'}, 
                    status=400
                )
        
        # Get Shehia and Bin
        try:
            shehia = Shehia.objects.get(id=data['shehia_id'])
            bin_obj = Bin.objects.get(id=data['bin_id'], shehia=shehia)
        except (Shehia.DoesNotExist, Bin.DoesNotExist):
            return JsonResponse(
                {'success': False, 'error': 'Invalid shehia or bin'}, 
                status=400
            )
        
        # Create WasteReport (accept both `description` and legacy `comment`)
        description = data.get('description', data.get('comment', ''))
        waste_level = data.get('waste_level', 'unknown')

        report = WasteReport.objects.create(
            shehia=shehia,
            bin=bin_obj,
            timestamp=data['timestamp'],
            comment=description,
            waste_level=waste_level,
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Report submitted successfully',
            'report_id': report.id
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_waste_reports(request):
    """Get list of all waste reports"""
    try:
        qs = WasteReport.objects.all().values(
            'id', 'shehia__name', 'bin__name', 'bin__location',
            'timestamp', 'comment', 'waste_level', 'submitted_at'
        )

        data = []
        for r in qs:
            data.append({
                'id': r['id'],
                'timestamp': r['timestamp'],
                'shehia': r['shehia__name'],
                'bin': r['bin__name'],
                'bin_location': r.get('bin__location'),
                'waste_level': r.get('waste_level', 'unknown'),
                'description': r.get('comment', ''),
                'submitted_at': r.get('submitted_at'),
            })

        return JsonResponse({
            'success': True,
            'data': data,
            'count': WasteReport.objects.count()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_optimization_schedule(request):
    """Get optimized collection schedule based on predictions and community reports."""
    global MODEL_PIPELINE, MODEL_PREDICT_FUNC
    if MODEL_PIPELINE is None:
        try:
            from .model_utils import load_pipeline, predict_waste_level

            MODEL_PIPELINE = load_pipeline(MODEL_PATH)
            MODEL_PREDICT_FUNC = predict_waste_level
        except Exception as exc:
            return JsonResponse({'success': False, 'error': 'Model not loaded.', 'details': str(exc)}, status=500)

    try:
        schedule = build_optimization_schedule(MODEL_PIPELINE)
        return JsonResponse({'success': True, 'data': schedule})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def _create_pdf_timetable(timetable, selected_date):
    def escape_pdf(text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)').replace('\n', ' ')

    date_title = f"Collection Timetable for {selected_date.strftime('%Y-%m-%d')}"
    lines = [date_title, '']
    lines.append('Time    Shehia    Bin    Priority    Prediction')
    lines.append('')
    for row in timetable:
        lines.append(f"{row['time']}    {row['shehia']}    {row['bin']}    {row['priority']}    {row['prediction']}")

    stream_lines = [
        'BT',
        '/F1 10 Tf',
        '50 760 Td',
        '0 -14 Td',
    ]
    for i, line in enumerate(lines):
        stream_lines.append(f"({escape_pdf(line)}) Tj")
        if i < len(lines) - 1:
            stream_lines.append('0 -14 Td')
    stream_lines.append('ET')
    stream = '\n'.join(stream_lines).encode('latin-1')

    objects = []
    objects.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
    objects.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
    objects.append(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n')
    objects.append(b'4 0 obj\n<< /Length %d >>\nstream\n' % len(stream) + stream + b'\nendstream\nendobj\n')
    objects.append(b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')

    xref = []
    current_pos = 0
    header = b'%PDF-1.4\n'
    current_pos += len(header)
    pdf_body = header
    for obj in objects:
        xref.append(current_pos)
        pdf_body += obj
        current_pos += len(obj)

    xref_start = current_pos
    xref_body = b'xref\n0 %d\n0000000000 65535 f \n' % (len(objects) + 1)
    for offset in xref:
        xref_body += b'%010d 00000 n \n' % offset
    trailer = b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objects) + 1, xref_start)
    pdf_body += xref_body + trailer
    return pdf_body


@require_http_methods(["GET"])
def optimization_dashboard(request):
    """Render the backend optimization dashboard."""
    global MODEL_PIPELINE, MODEL_PREDICT_FUNC
    if MODEL_PIPELINE is None:
        try:
            from .model_utils import load_pipeline, predict_waste_level

            MODEL_PIPELINE = load_pipeline(MODEL_PATH)
            MODEL_PREDICT_FUNC = predict_waste_level
        except Exception as exc:
            return render(request, 'prediction/optimization_dashboard.html', {
                'error': f'Model not loaded: {exc}'
            })

    latest_saved_batch = SavedPredictionBatch.objects.order_by('-created_at').first()
    try:
        if latest_saved_batch is not None:
            schedule = build_optimization_schedule(saved_batch=latest_saved_batch)
        else:
            schedule = build_optimization_schedule(MODEL_PIPELINE)
    except Exception as exc:
        return render(request, 'prediction/optimization_dashboard.html', {
            'error': str(exc)
        })

    view_timetable = request.GET.get('view_timetable') == '1'

    shehia_filter = request.GET.get('shehia', '').strip()
    bin_filter = request.GET.get('bin', '').strip()
    priority_filter = request.GET.get('priority', '').strip()
    selected_date = request.GET.get('date', '').strip()

    today = timezone.localdate()
    selected_all = False
    if selected_date and selected_date.lower() == 'all':
        selected_all = True
        selected_date_dt = None
    else:
        if selected_date:
            try:
                selected_date_dt = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
            except ValueError:
                selected_date_dt = today
        else:
            selected_date_dt = today

    base_filters = {
        'shehia': shehia_filter,
        'bin': bin_filter,
        'priority': priority_filter,
    }

    # Attach per-item selected-day forecast (or leave daily_forecast intact when `All` selected)
    for item in schedule:
        if selected_all:
            item['selected_day_forecast'] = None
            item['selected_day_priority'] = None
        else:
            selected_forecast = next(
                (
                    forecast for forecast in item.get('daily_forecast', [])
                    if forecast.get('date') == selected_date_dt.strftime('%Y-%m-%d')
                ),
                None,
            )
            if selected_forecast:
                item['selected_day_forecast'] = selected_forecast
                item['selected_day_priority'], _ = _map_prediction_to_priority(
                    selected_forecast.get('prediction', 'unknown')
                )
            else:
                item['selected_day_forecast'] = {
                    'prediction': '-',
                    'date': selected_date_dt.strftime('%Y-%m-%d'),
                }
                item['selected_day_priority'] = item.get('priority', 'Low')

    # Apply shehia/bin filters (these filter the items themselves regardless of day/all)
    if shehia_filter:
        schedule = [
            item for item in schedule
            if shehia_filter.lower() in item['shehia'].lower()
        ]

    if bin_filter:
        schedule = [
            item for item in schedule
            if bin_filter.lower() in item['bin'].lower()
        ]

    # Priority filter behavior differs for All vs single-day selection
    if priority_filter and priority_filter.lower() != 'all':
        if selected_all:
            # Keep items where any day matches the chosen priority
            def item_matches_priority_anyday(item):
                for f in item.get('daily_forecast', []):
                    p, _ = _map_prediction_to_priority(f.get('prediction', 'unknown'))
                    if p.lower() == priority_filter.lower():
                        return True
                return False

            schedule = [item for item in schedule if item_matches_priority_anyday(item)]
        else:
            schedule = [
                item for item in schedule
                if item['selected_day_priority'].lower() == priority_filter.lower()
            ]

    # Summary counts
    summary = {'high': 0, 'medium': 0, 'low': 0}
    if selected_all:
        # Aggregate across all forecasts
        for item in schedule:
            for f in item.get('daily_forecast', []):
                p, _ = _map_prediction_to_priority(f.get('prediction', 'unknown'))
                if p.lower() == 'high':
                    summary['high'] += 1
                elif p.lower() == 'medium':
                    summary['medium'] += 1
                else:
                    summary['low'] += 1
    else:
        for item in schedule:
            priority_key = item['selected_day_priority'].lower()
            if priority_key == 'high':
                summary['high'] += 1
            elif priority_key == 'medium':
                summary['medium'] += 1
            else:
                summary['low'] += 1

    def build_date_url(target):
        params = base_filters.copy()
        if isinstance(target, str) and target == 'all':
            params['date'] = 'all'
        else:
            params['date'] = target.strftime('%Y-%m-%d')
        return f"{request.path}?{urlencode(params)}"

    # Day buttons: include 'All' then actual forecast dates from the first schedule item if available
    day_buttons = [
        {
            'label': 'All',
            'date': 'all',
            'url': build_date_url('all'),
            'is_active': selected_all,
        }
    ]
    if schedule and schedule[0].get('daily_forecast'):
        for forecast in schedule[0]['daily_forecast']:
            day_dt = timezone.datetime.strptime(forecast['date'], '%Y-%m-%d').date()
            day_buttons.append({
                'label': forecast.get('formatted_date', forecast['date']),
                'date': day_dt,
                'url': build_date_url(day_dt),
                'is_active': (not selected_all and day_dt == selected_date_dt),
            })
    else:
        for offset, label in [(0, 'Today'), (1, 'Tomorrow'), (2, 'Day After Tomorrow'), (3, 'Third Day')]:
            day_dt = today + timedelta(days=offset)
            day_buttons.append({
                'label': label,
                'date': day_dt,
                'url': build_date_url(day_dt),
                'is_active': (not selected_all and day_dt == selected_date_dt),
            })

    timetable = []
    download_url_csv = None
    download_url_pdf = None
    view_timetable_url = None
    show_timetable = view_timetable and not selected_all
    if not selected_all:
        high_priority_items = []
        for item in schedule:
            forecast = item.get('selected_day_forecast', {})
            prediction_text = str(forecast.get('prediction', '')).lower()
            if item.get('selected_day_priority') == 'High' or prediction_text in ['high', 'full']:
                high_priority_items.append(item)

        time_base = datetime(
            selected_date_dt.year,
            selected_date_dt.month,
            selected_date_dt.day,
            8,
            0,
        )
        for index, item in enumerate(high_priority_items):
            slot = time_base + timedelta(minutes=30 * index)
            timetable.append({
                'time': slot.strftime('%H:%M'),
                'shehia': item['shehia'],
                'bin': item['bin'],
                'priority': 'High',
                'prediction': item.get('selected_day_forecast', {}).get('prediction', '-'),
            })

        if timetable:
            params = base_filters.copy()
            params['date'] = selected_date_dt.strftime('%Y-%m-%d')
            params['view_timetable'] = '1'
            view_timetable_url = f"{request.path}?{urlencode(params)}"
            download_url_csv = f"{request.path}?{urlencode({**params, 'download_timetable': 'csv'})}"
            download_url_pdf = f"{request.path}?{urlencode({**params, 'download_timetable': 'pdf'})}"

    download_format = request.GET.get('download_timetable')
    if download_format in ('csv', 'pdf') and timetable:
        if download_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="timetable_%s.csv"' % selected_date_dt.strftime('%Y-%m-%d')
            writer = csv.writer(response)
            writer.writerow(['Time of Collection', 'Shehia', 'Bin', 'Priority', 'Prediction'])
            for row in timetable:
                writer.writerow([row['time'], row['shehia'], row['bin'], row['priority'], row['prediction']])
            return response
        else:
            pdf_data = _create_pdf_timetable(timetable, selected_date_dt)
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="timetable_%s.pdf"' % selected_date_dt.strftime('%Y-%m-%d')
            return response

    return render(request, 'prediction/optimization_dashboard.html', {
        'schedule': schedule,
        'summary': summary,
        'day_buttons': day_buttons,
        'selected_date': selected_date_dt,
        'selected_all': selected_all,
        'filters': base_filters,
        'latest_saved_batch': latest_saved_batch,
        'timetable': timetable,
        'view_timetable_url': view_timetable_url,
        'download_url_csv': download_url_csv,
        'download_url_pdf': download_url_pdf,
        'show_timetable': show_timetable,
    })


@require_http_methods(["GET"])
def record_collections(request):
    """Record a successful collection for all bins."""
    bins = Bin.objects.select_related('shehia').all()
    records = []
    for bin_obj in bins:
        records.append(CollectionRecord(shehia=bin_obj.shehia, bin=bin_obj, status='collected'))

    CollectionRecord.objects.bulk_create(records)
    return render(request, 'prediction/record_collections.html', {
        'record_count': len(records),
        'records': records,
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_waste_report(request, report_id):
    """Delete a waste report"""
    try:
        report = WasteReport.objects.get(id=report_id)
        report.delete()
        return JsonResponse({'success': True, 'message': 'Report deleted successfully'})
    except WasteReport.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def report_page(request):
    """Render the React-based waste report page."""
    return render(request, "prediction/react_report_page.html")


@require_http_methods(["GET"])
def admin_dashboard(request):
    """Render the waste reports admin dashboard."""
    return render(request, "prediction/admin_dashboard.html")


@require_http_methods(["GET"])
def statistics_dashboard(request):
    """Render the statistics and analytics dashboard."""
    from collections import Counter
    from django.db.models import Count, Q
    
    # Waste Level Distribution
    waste_levels = WasteReport.objects.values('waste_level').annotate(count=Count('id'))
    waste_level_chart = {
        'labels': [item['waste_level'].title() for item in waste_levels],
        'data': [item['count'] for item in waste_levels],
    }
    
    # Reports by Shehia
    shehia_reports = WasteReport.objects.values('shehia__name').annotate(count=Count('id')).order_by('-count')[:10]
    shehia_chart = {
        'labels': [item['shehia__name'] for item in shehia_reports],
        'data': [item['count'] for item in shehia_reports],
    }
    
    # High/Full reports by Shehia
    high_full_by_shehia = WasteReport.objects.filter(waste_level__in=['high', 'full']).values('shehia__name').annotate(count=Count('id')).order_by('-count')[:10]
    high_full_chart = {
        'labels': [item['shehia__name'] for item in high_full_by_shehia],
        'data': [item['count'] for item in high_full_by_shehia],
    }
    
    # Reports by Bin (top 10)
    bin_reports = WasteReport.objects.values('bin__name').annotate(count=Count('id')).order_by('-count')[:10]
    bin_chart = {
        'labels': [item['bin__name'] for item in bin_reports],
        'data': [item['count'] for item in bin_reports],
    }
    
    # Summary Statistics
    total_reports = WasteReport.objects.count()
    total_full = WasteReport.objects.filter(waste_level='full').count()
    total_high = WasteReport.objects.filter(waste_level='high').count()
    total_shehias = Shehia.objects.count()
    total_bins = Bin.objects.count()
    
    # Optimization Schedule Summary
    try:
        optimization_summary = {'high': 0, 'medium': 0, 'low': 0}
        latest_saved_batch = SavedPredictionBatch.objects.order_by('-created_at').first()
        if latest_saved_batch is not None:
            schedule = build_optimization_schedule(saved_batch=latest_saved_batch)
            optimization_summary = {
                'high': sum(1 for item in schedule if item['priority'] == 'High'),
                'medium': sum(1 for item in schedule if item['priority'] == 'Medium'),
                'low': sum(1 for item in schedule if item['priority'] == 'Low'),
            }
        else:
            pipeline = None
            try:
                from .model_utils import load_pipeline
                pipeline = load_pipeline(MODEL_PATH)
            except:
                pass
            if pipeline:
                try:
                    schedule = build_optimization_schedule(pipeline)
                    optimization_summary = {
                        'high': sum(1 for item in schedule if item['priority'] == 'High'),
                        'medium': sum(1 for item in schedule if item['priority'] == 'Medium'),
                        'low': sum(1 for item in schedule if item['priority'] == 'Low'),
                    }
                except:
                    pass
    except:
        optimization_summary = {'high': 0, 'medium': 0, 'low': 0}
    
    context = {
        'total_reports': total_reports,
        'total_full': total_full,
        'total_high': total_high,
        'total_shehias': total_shehias,
        'total_bins': total_bins,
        'waste_level_chart': waste_level_chart,
        'shehia_chart': shehia_chart,
        'high_full_chart': high_full_chart,
        'bin_chart': bin_chart,
        'optimization_summary': optimization_summary,
    }
    
    return render(request, "prediction/statistics_dashboard.html", context)
