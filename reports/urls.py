from django.urls import path

from .views import (SalaryRangeMonthView, LocationReportView, ResidenceReportView,
                    get_all_months_details, get_all_vacations_details, get_single_month_attendance_details)


urlpatterns = [
    path('residence-range/', ResidenceReportView.as_view(), name='residence_range'),
    path('salary-range-month/', SalaryRangeMonthView.as_view(), name='salary_range_month'),
    path('location-exact-month/', LocationReportView.as_view(), name='location_exact_month'),

    path('api/get_all_months_details/<int:worker_id>', get_all_months_details, name='get_all_months_details'),
    path('api/get_all_vacations_details/<int:worker_id>', get_all_vacations_details, name='get_all_vacations_details'),
    path('api/single_month_attendance_details/<int:month_id>', get_single_month_attendance_details, name='single_month_attendance_details'),
]
