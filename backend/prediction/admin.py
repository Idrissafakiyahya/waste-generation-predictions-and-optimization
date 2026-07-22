from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta
from django import forms
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from .models import Shehia, Bin, WasteReport, SavedPredictionBatch, SavedPredictionItem, CollectionRecord
from .optimization import build_three_day_forecasts

MODEL_PATH = Path(__file__).resolve().parent.parent / "waste_model.pkl"
MODEL_PIPELINE = None
MODEL_PREDICT_FUNC = None


class PredictionForm(forms.Form):
    Timestamp = forms.CharField(
        label="Timestamp",
        max_length=100,
        initial="2026-07-01T10:00:00Z",
        widget=forms.TextInput(attrs={"size": 40}),
    )
    Shehia = forms.CharField(label="Shehia", max_length=100, initial="Amani")
    Bin = forms.CharField(label="Bin", max_length=100, initial="AmaniA")


def load_pipeline():
    global MODEL_PIPELINE, MODEL_PREDICT_FUNC
    if MODEL_PIPELINE is None:
        from .model_utils import load_pipeline as _load_pipeline, predict_waste_level

        MODEL_PIPELINE = _load_pipeline(MODEL_PATH)
        MODEL_PREDICT_FUNC = predict_waste_level
    return MODEL_PIPELINE, MODEL_PREDICT_FUNC


def prediction_view(request):
    """Django admin view for model predictions"""
    weekly_result = None
    error = None
    save_message = None
    form = PredictionForm(request.POST or None)

    if request.method == "POST":
        action = request.POST.get("action")
        MODEL_PIPELINE, MODEL_PREDICT_FUNC = load_pipeline()

        if action == "weekly_predict":
            try:
                weekly_result = build_three_day_forecasts(MODEL_PIPELINE)
            except Exception as exc:
                error = str(exc)
        elif action == "save_predictions":
            try:
                weekly_result = build_three_day_forecasts(MODEL_PIPELINE)
                batch = save_prediction_batch(weekly_result)
                item_count = batch.items.count()
                save_message = f"✓ Successfully saved {item_count} predictions in batch {batch.id} at {batch.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            except Exception as exc:
                error = str(exc)
        elif form.is_valid():
            result = MODEL_PREDICT_FUNC(
                MODEL_PIPELINE,
                form.cleaned_data["Timestamp"],
                form.cleaned_data["Shehia"],
                form.cleaned_data["Bin"],
            )
            return render(
                request,
                "prediction/admin_prediction.html",
                {"form": form, "result": result},
            )
        else:
            error = "Please provide valid timestamp, shehia, and bin values."

    return render(
        request,
        "prediction/admin_prediction.html",
        {"form": form, "weekly_result": weekly_result, "error": error, "save_message": save_message},
    )


def save_prediction_batch(forecast_data, name=None):
    batch_name = name or f"Prediction batch {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    with transaction.atomic():
        batch = SavedPredictionBatch.objects.create(name=batch_name)
        items = []
        for item in forecast_data:
            for forecast in item["daily_forecast"]:
                items.append(
                    SavedPredictionItem(
                        batch=batch,
                        shehia=item["shehia"],
                        bin=item["bin"],
                        day_label=forecast["label"],
                        date=datetime.strptime(forecast["date"], "%Y-%m-%d").date(),
                        formatted_date=forecast["formatted_date"],
                        prediction=forecast["prediction"],
                        probabilities=forecast.get("probabilities", {}),
                    )
                )
        SavedPredictionItem.objects.bulk_create(items)
    return batch


def predicted_data_view(request):
    batches = SavedPredictionBatch.objects.prefetch_related("items").order_by("-created_at")

    # Handle delete action
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete_batch":
            batch_id = request.POST.get("batch_id")
            if batch_id:
                batch = SavedPredictionBatch.objects.filter(pk=batch_id).first()
                if batch:
                    count = batch.items.count()
                    batch.delete()
                    messages.success(request, f"Deleted batch {batch_id} and its {count} items.")
                    return redirect(request.path)
                else:
                    messages.error(request, "Batch not found.")
            else:
                messages.error(request, "No batch selected to delete.")

    batch_id = request.GET.get("batch")
    selected_batch = None
    if batch_id:
        selected_batch = get_object_or_404(SavedPredictionBatch, pk=batch_id)
    elif batches:
        selected_batch = batches.first()

    return render(
        request,
        "prediction/saved_prediction_data.html",
        {"batches": batches, "selected_batch": selected_batch},
    )




# ============================================
# ADMIN REGISTRATIONS
# ============================================

@admin.register(Shehia)
class ShehiaAdmin(admin.ModelAdmin):
    change_list_template = 'prediction/shehia_change_list.html'
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    change_list_template = 'prediction/bin_change_list.html'
    list_display = ('name', 'shehia', 'location', 'capacity')
    list_filter = ('shehia',)
    search_fields = ('name', 'location')
    ordering = ('shehia', 'name')
    exclude = ('bin_type',)


@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    change_list_template = 'prediction/wastereport_change_list.html'
    list_display = ('id', 'shehia', 'bin', 'timestamp', 'waste_level', 'submitted_at')
    list_filter = ('shehia', 'bin', 'waste_level', 'submitted_at')
    search_fields = ('comment',)
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(CollectionRecord)
class CollectionRecordAdmin(admin.ModelAdmin):
    list_display = ('shehia', 'bin', 'collected_at', 'status')
    list_filter = ('status', 'shehia', 'bin')
    search_fields = ('shehia__name', 'bin__name')
    ordering = ('-collected_at',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        high_full_reports = WasteReport.objects.filter(waste_level__in=['high', 'full']).select_related('shehia', 'bin').order_by('bin__name', 'timestamp')
        alert_map = defaultdict(list)
        for report in high_full_reports:
            report_day = report.timestamp.date()
            alert_map[(report.bin.id, report_day)].append(report)

        alert_reports = []
        for (_, report_day), reports in alert_map.items():
            if len(reports) > 2:
                alert_reports.append({
                    'date': report_day,
                    'shehia': reports[0].shehia.name,
                    'bin': reports[0].bin.name,
                    'count': len(reports),
                    'levels': [r.waste_level for r in reports],
                    'comments': [r.comment or 'No comment' for r in reports],
                })

        extra_context['summary_full'] = high_full_reports.filter(waste_level='full').count()
        extra_context['summary_high'] = high_full_reports.filter(waste_level='high').count()
        extra_context['alert_reports'] = alert_reports
        return super().changelist_view(request, extra_context=extra_context)
