from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from prediction.admin import prediction_view, predicted_data_view
from prediction.views import report_page, optimization_dashboard, statistics_dashboard, record_collections

urlpatterns = [
    path("report/", report_page, name="report-page"),
    # Redirect root to admin dashboard
    path("", RedirectView.as_view(url='/admin/')),
    path("prediction/statistics/", admin.site.admin_view(statistics_dashboard), name="prediction-statistics"),
    path("admin/predict/", admin.site.admin_view(prediction_view), name="admin-predict"),
    path("admin/predicted-data/", admin.site.admin_view(predicted_data_view), name="admin-predicted-data"),
    path("admin/optimization/", admin.site.admin_view(optimization_dashboard), name="admin-optimization"),
    path("admin/record-collections/", admin.site.admin_view(record_collections), name="admin-record-collections"),
    path("admin/statistics/", admin.site.admin_view(statistics_dashboard), name="admin-statistics"),
    path("admin/", admin.site.urls),
    path("api/", include("prediction.urls")),
]
