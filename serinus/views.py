# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

@csrf_exempt
def properties(request):
    pass

def test_read(request):
    offset = 0
    limit = 1
    all = TemperatureRecord.objects.all()[offset:limit]
    return JsonResponse(data={}, status=200)
