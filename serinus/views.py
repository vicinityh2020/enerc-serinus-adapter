# Create your views here.
from django.http import JsonResponse
from .models import DecimalRecord, MetaData, Sensor


def test_write(request):
    record = {
        "Origin Network Level": 1,
        "packet type": 2,
        "Hardware version": "2.0",
        "Hop Counter": 1,
        "Value": False,
        "System ID": "10.0.0.12",
        "software ver": "2.1",
        "voltage": 3.21,
        "Sensor": "Humidity",
        "Message counter": 37250,
        "Timestamp": 1544313183.160063,
        "Origin ID": "0.62.3.0",
        "RSSI": 150,
        "GW_MAC": "6D:F6:55:4E:AB:C0",
        "Latency counter": 7
    }

    sensor_type = record['Sensor']
    rssi = record['RSSI']
    voltage = record['voltage']

    sv = record['software ver']
    mc = record['Message counter']

    value = record['Value']

    meta_data = MetaData(software_version=sv, message_counter=mc)
    sensor = Sensor(rssi=rssi, voltage=voltage, sensor_type=sensor_type)

    r = DecimalRecord(value=value, meta_data=meta_data, sensor=sensor)
    r.save()

    return JsonResponse(data={}, status=200)


def test_read(request):
    offset = 0
    limit = 1
    all = DecimalRecord.objects.all()[offset:limit]
    return JsonResponse(data={}, status=200)
