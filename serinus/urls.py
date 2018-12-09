from django.urls import path
from . import views

urlpatterns = [
    path('testw', views.test_write),
    path('testr', views.test_read),
]