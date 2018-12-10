from django.contrib import admin
from .models import *

admin.site.register([TemperatureRecord, NoiseRecord, CO2Record, MovementRecord, LightRecord, HumidityRecord])
