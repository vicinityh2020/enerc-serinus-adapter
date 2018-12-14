# Create your views here.
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import *


@csrf_exempt
@require_http_methods(['POST'])
def properties(request, oid, pid):
    response = {
        'error': None,
        'body': [],
    }

    try:
        sensor = SensorConfig.objects.get(vicinity_oid=oid)
    except SensorConfig.DoesNotExist:
        response['error'] = {
            'message': ('object %s does not exist in the database' % oid),
            'status': 404,
        }
        return JsonResponse(data=response, status=404)

    paging = json.loads(request.body.decode('utf-8'))

    offset = int(paging['offset']) if 'offset' in paging else 0
    limit = int(paging['limit']) if 'limit' in paging else settings.MAX_LIMIT

    if limit < 1:
        response['error'] = {
            'message': 'limit must be greater than 0',
            'status': 401,
        }
        return JsonResponse(data=response, status=404)
    elif offset < 1:
        response['error'] = {
            'message': 'offset must be greater than 0',
            'status': 401,
        }
        return JsonResponse(data=response, status=404)

    cap = offset + limit

    if pid == settings.PROPERTY_CO2:
        records = CO2Record.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    elif pid == settings.PROPERTY_MOVEMENT:
        records = MovementRecord.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    elif pid == settings.PROPERTY_HUMIDITY:
        records = HumidityRecord.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    elif pid == settings.PROPERTY_TEMPERATURE:
        records = TemperatureRecord.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    elif pid == settings.PROPERTY_LIGHT:
        records = LightRecord.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    elif pid == settings.PROPERTY_NOISE:
        records = NoiseRecord.objects.filter(meta_data={'origin_id': sensor.origin_id})[offset:cap]

    else:
        response['error'] = {
            'message': ('object %s has no property named %s' % (oid, pid)),
            'status': 404,
        }
        return JsonResponse(data=response, status=404)

    for r in records:
        entry = {'value': r.value, 'timestamp': r.timestamp.timestamp()}
        response['body'].append(entry)

    return JsonResponse(data=response, status=200)


def make_prop(oid, pid, value_type):

    return {
        "pid": pid,
        "monitors": "adapters:DeviceStatus",
        "read_link": {
            "href": "/objects/%s/properties/%s" % (oid, pid),
            "output": {
                "type": "object",
                "field": [
                    {
                        "name": "timestamp",
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "value",
                        "schema": {
                            "type": value_type
                        }
                    }
                ]
            }
        },
    }


def thing_description(request):
    all_sensors = SensorConfig.objects.all()
    td = settings.THING_DESCRIPTION

    for sensor in all_sensors:
        device = dict()
        device['oid'] = sensor.vicinity_oid
        device['name'] = 'sensor:%s' % sensor.origin_id
        device['type'] = 'core:Device'

        device['properties'] = list()
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_TEMPERATURE, 'number'))
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_HUMIDITY, 'number'))
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_LIGHT, 'integer'))
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_NOISE, 'number'))
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_MOVEMENT, 'boolean'))
        device['properties'].append(make_prop(sensor.vicinity_oid, settings.PROPERTY_CO2, 'number'))

        device['actions'] = []
        device['event'] = []

        td['thing-descriptions'].append(device)

    return JsonResponse(data=td, status=200)
