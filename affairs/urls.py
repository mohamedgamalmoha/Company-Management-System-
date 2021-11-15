from django.urls import path

from main_reports.urls import urlpatterns as main_repo_urls
from .views import (home, MonthCreationView, MonthDetailView, ActivityCreationView, ActivityDetailView,
                    LocationCreationView, LocationDetailView, VacationsCreationView, VacationsDetailView,
                    MonthListView, ActivityListView, LocationListView, VacationsListView, MonthDayInlineView,
                    validate_month_uniqueness)


app_name = 'affairs'


urlpatterns = [
    path('', home, name='home'),
    *main_repo_urls,

    path('month-list/', MonthListView.as_view(), name='month_list'),
    path('month-creation/', MonthCreationView.as_view(), name='month_creation'),
    path('month-detail/<int:pk>/', MonthDetailView.as_view(), name='month_detail'),
    path('month-day-inline/<int:pk>', MonthDayInlineView.as_view(), name='month_day_inline'),

    path('activity-list/', ActivityListView.as_view(), name='activity_list'),
    path('activity-creation/', ActivityCreationView.as_view(), name='activity_creation'),
    path('activity-detail/<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),

    path('location-list/', LocationListView.as_view(), name='location_list'),
    path('location-creation/', LocationCreationView.as_view(), name='location_creation'),
    path('location-detail/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),

    path('vacations_list/', VacationsListView.as_view(), name='vacations_list'),
    path('vacations-creation/', VacationsCreationView.as_view(), name='vacations_creation'),
    path('vacations-detail/<int:pk>/', VacationsDetailView.as_view(), name='vacations_detail'),

    path('month_uniqueness/', validate_month_uniqueness, name='month_uniqueness'),
]
