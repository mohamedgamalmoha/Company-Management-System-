from django.urls import path

from .views import home
from reports.urls import urlpatterns as repo_urls


app_name = 'affairs'

urlpatterns = [
    path('', home, name='home'),
    *repo_urls,
]
