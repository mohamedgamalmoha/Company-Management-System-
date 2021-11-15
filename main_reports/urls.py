from django.urls import path
from .views import (MultiWorkerReportView, AccommodationReportView, MultiWorkerReportPrintView,
                    SingleMonthReportView, SingleMonthReportPrintView)


urlpatterns = [
    path('multi-worker-report/', MultiWorkerReportView.as_view(), name='multi_worker_report'),
    path('multi-worker-report-print/', MultiWorkerReportPrintView.as_view(), name='multi_worker_report_print'),

    path('single-month-report/', SingleMonthReportView.as_view(), name='single_month_report'),
    path('single-month-report-print/<int:pk>/', SingleMonthReportPrintView.as_view(), name='single_month_report_print'),

    path('accommodation-report/', AccommodationReportView.as_view(), name='accommodation_report'),
]
