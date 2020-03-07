from django.contrib import admin
from django.urls import path, include

from Dashboard import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('test/<str:test_var>', views.test_with_var),
    path('test', views.test),
    path('aircraft/', views.aircrafts),
    path('aircraft/<str:aircraftid>', views.aircraft),
    path('flight/<int:day>/<int:month>/<int:year>', views.flight),
]
