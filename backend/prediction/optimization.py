from datetime import datetime, timedelta
from django.utils import timezone
from .models import WasteReport, SavedPredictionBatch
from .model_utils import predict_waste_level


def _map_prediction_to_priority(prediction_label):
    label = str(prediction_label).strip().lower()
    if 'full' in label or 'high' in label:
        return 'High', 1
    if 'medium' in label:
        return 'Medium', 2
    if 'low' in label or 'empty' in label:
        return 'Low', 3
    return 'Normal', 3


def build_three_day_forecasts(pipeline):
    """Build a shared 3-day forecast data set from the latest community reports."""
    latest_reports = {}
    reports = WasteReport.objects.select_related('shehia', 'bin').order_by('shehia__name', 'bin__name', '-timestamp')

    for report in reports:
        key = (report.shehia.name, report.bin.name)
        if key not in latest_reports:
            latest_reports[key] = report

    if not latest_reports:
        raise ValueError('No community reports are available for prediction.')

    predictions = []
    day_labels = ['Tomorrow', 'Day After Tomorrow', 'Third Day']
    today = timezone.localdate()
    for report in latest_reports.values():
        daily_forecast = []

        for day_offset, label in enumerate(day_labels, start=1):
            future_date = today + timedelta(days=day_offset)
            future_ts = future_date.strftime('%Y-%m-%dT00:00:00Z')
            prediction = predict_waste_level(
                pipeline,
                future_ts,
                report.shehia.name,
                report.bin.name,
            )
            predicted_level = prediction.get('prediction', 'unknown')
            daily_forecast.append({
                'label': label,
                'date': future_date.strftime('%Y-%m-%d'),
                'formatted_date': future_date.strftime('%a, %B %d'),
                'prediction': predicted_level,
                'probabilities': prediction.get('probabilities', {}),
            })

        predictions.append({
            'shehia': report.shehia.name,
            'bin': report.bin.name,
            'current_report_level': report.waste_level,
            'daily_forecast': daily_forecast,
        })

    return sorted(predictions, key=lambda item: (item['shehia'], item['bin']))


def build_optimization_schedule(pipeline=None, saved_batch=None):
    """Build an optimization schedule from saved prediction data or latest community reports."""
    if saved_batch is not None:
        latest_reports = {}
        reports = WasteReport.objects.select_related('shehia', 'bin').order_by('shehia__name', 'bin__name', '-timestamp')
        for report in reports:
            key = (report.shehia.name, report.bin.name)
            if key not in latest_reports:
                latest_reports[key] = report

        forecast_data = []
        batch_items = saved_batch.items.all().order_by('shehia', 'bin', 'date')
        grouped = {}
        for item in batch_items:
            key = (item.shehia, item.bin)
            grouped.setdefault(key, []).append(item)

        for (shehia, bin_name), items in grouped.items():
            current_report = latest_reports.get((shehia, bin_name))
            current_report_level = current_report.waste_level if current_report else 'unknown'
            daily_forecast = [
                {
                    'label': item.day_label,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'formatted_date': item.formatted_date,
                    'prediction': item.prediction,
                    'probabilities': item.probabilities or {},
                }
                for item in items
            ]
            forecast_data.append({
                'shehia': shehia,
                'bin': bin_name,
                'current_report_level': current_report_level,
                'daily_forecast': daily_forecast,
            })
    else:
        if pipeline is None:
            raise ValueError('No prediction pipeline or saved batch available for optimization.')
        forecast_data = build_three_day_forecasts(pipeline)

    schedule = []
    for item in forecast_data:
        highest_priority = ('Low', 3)
        first_collection_day = None

        for forecast in item['daily_forecast']:
            priority, weight = _map_prediction_to_priority(forecast.get('prediction', 'unknown'))
            if priority == 'High' and first_collection_day is None:
                first_collection_day = forecast['date']
            if weight < highest_priority[1]:
                highest_priority = (priority, weight)

        if first_collection_day is None and item['daily_forecast']:
            first_collection_day = item['daily_forecast'][-1]['date']

        schedule.append({
            'shehia': item['shehia'],
            'bin': item['bin'],
            'current_report_level': item.get('current_report_level', 'unknown'),
            'priority': highest_priority[0],
            'recommended_collection': first_collection_day,
            'daily_forecast': item['daily_forecast'],
        })

    return sorted(schedule, key=lambda item: (item['priority'], item['shehia'], item['bin']))
