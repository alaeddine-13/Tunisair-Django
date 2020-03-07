from django.contrib import admin
from django.urls import path, include

from Dashboard import views

urlpatterns = [
    path('api/', include('Dashboard.urls')),
]
