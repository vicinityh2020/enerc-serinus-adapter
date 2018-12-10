from django.urls import path
from . import views

urlpatterns = [
    path('objects/<oid>/properties/<pid>', views.properties, name='properties'),
    path('objects', views.properties, name='thing_description'),
    path('testr', views.test_read),
]