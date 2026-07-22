from django.urls import path
from .views import predict, get_shehias, get_bins, submit_waste_report, get_waste_reports, admin_dashboard, delete_waste_report, get_optimization_schedule, statistics_dashboard

urlpatterns = [
    path("predict/", predict, name="predict"),
    path("shehias/", get_shehias, name="get-shehias"),
    path("bins/", get_bins, name="get-bins"),
    path("reports/", submit_waste_report, name="submit-report"),
    path("reports/list/", get_waste_reports, name="list-reports"),
    path("reports/<int:report_id>/delete/", delete_waste_report, name="delete-report"),
    path("optimization/schedule/", get_optimization_schedule, name="optimization-schedule"),
    path("dashboard/", admin_dashboard, name="admin-dashboard"),
    path("statistics/", statistics_dashboard, name="statistics-dashboard"),
]
