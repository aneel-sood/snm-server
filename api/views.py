from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.models import Resource
from api.serializers import ResourceSerializer

@csrf_exempt
def resources(request):
    if request.method == 'GET':
        type = request.GET.get('type', '')
        resources = Resource.objects.filter(type=type)
        serializer = ResourceSerializer(resources, many=True)
        return JsonResponse(serializer.data, safe=False)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = ResourceSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)
