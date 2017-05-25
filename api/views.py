from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from json import loads
from api.models import Resource, Provider
from api.serializers import ResourceSerializer, ProviderSerializer
from django.db.models import Q

@csrf_exempt
def providers(request):
    if request.method == 'GET':
      params = loads(request.GET.get('params', '{}'))
      
      q_objects = Q()
      for param_name, value in params['details'].items():
        q_objects.add(Q(**{'{0}__{1}__{2}'.format('resources', 'details', param_name): value}), Q.AND)

      providers = Provider.objects.filter(resources__type=params['resource_type']).filter(q_objects).distinct()

      serializer = ProviderSerializer(providers, many=True)
      return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def all_providers(request):
    if request.method == 'GET':
      providers = Provider.objects.all()
      serializer = ProviderSerializer(providers, many=True)
      return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def resources(request):
    if request.method == 'GET':
      params = loads(request.GET.get('params', '{}'))
      
      q_objects = Q()
      for param_name, value in params['details'].items():
        q_objects.add(Q(**{'{0}__{1}'.format('details', param_name): value}), Q.AND)

      resources = Resource.objects.filter(type=params['type']).filter(q_objects)
      serializer = ResourceSerializer(resources, many=True)
      return JsonResponse(serializer.data, safe=False)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = ResourceSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)
