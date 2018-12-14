from django.urls import path
from . import views

urlpatterns = [
    path('objects/<oid>/properties/<pid>', views.properties, name='properties'),
    path('objects', views.thing_description, name='thing_description'),
]