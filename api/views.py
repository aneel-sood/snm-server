from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from json import loads
from api.models import *
from api.serializers import *
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

@csrf_exempt
def resources(request):
  if request.method == 'GET':
    resources = Resource.objects.all()
    serializer = ResourceWithProviderSerializer(resources, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def resource(request, pk=None):
  if request.method == 'GET':
    resource = Resource.objects.get(pk=pk)
    serializer = ResourceWithProviderSerializer(resource)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'POST':
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)

    resource = Resource.objects.create(provider_id=params['provider_id'], type=params['type'], 
      details=params['details'])
    serializer = ResourceSerializer(resource)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'PUT': 
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)
      
    resource = Resource.objects.filter(pk=pk)
    resource.update(**params)
    serializer = ResourceSerializer(resource.first())
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'DELETE':
    resource = Resource.objects.filter(pk=pk).first()
    resource.delete()
    return JsonResponse({}, status=200)

@csrf_exempt
def providers(request):
  if request.method == 'GET':
    params = loads(request.GET.get('params', '{}'))

    if params:
      q_objects = Q()
      for param_name, value in params['details'].items():
        q_objects.add(Q(**{'{0}__{1}__{2}'.format('resources', 'details', param_name): value}), Q.AND)

      providers = Provider.objects.filter(resources__type=params['resource_type']).filter(q_objects).distinct()
      serializer = ProviderWithResourcesSerializer(providers, many=True)

    else: 
      providers = Provider.objects.all()
      serializer = ProviderSerializer(providers, many=True)

    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def provider(request, pk=None):
  if request.method == 'GET':
    provider = Provider.objects.get(pk=pk)
    serializer = ProviderSerializer(provider)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'POST':
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)

    provider = Provider.objects.create(first_name=params['first_name'], last_name=params['last_name'], email=params['email'])
    serializer = ProviderSerializer(provider)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'PUT': 
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)
      
    provider = Provider.objects.filter(pk=pk)
    provider.update(**params)
    serializer = ProviderSerializer(provider.first())
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'DELETE':
    provider = Provider.objects.filter(pk=pk).first()
    provider.delete()
    return JsonResponse({}, status=200)

@csrf_exempt
def dashboard_clients(request):
  if request.method == 'GET':
    two_weeks_ago = timezone.now() - timedelta(weeks=2)
    clients = Client.objects.filter(needs__needresourcematch__updated_at__gt = two_weeks_ago).distinct()
    serializer = DashboardClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def client_needs(request, client_id):
  # GET returns all needs for the specified Client
  if request.method == 'POST': # POST creates a new need for the specified Client   
    need = Need.objects.create(client_id=client_id)
    serializer = NeedResourceMatchStatusSerializer(need)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def client_need(request, client_id, pk):
  # GET returns the specific client need
  if request.method == 'PUT': 
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)
      
    need = Need.objects.filter(client_id = client_id, pk=pk).first()
    need.type=params['need_type']
    need.requirements=params['requirements']
    need.save()
    serializer = NeedResourceMatchStatusSerializer(need)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'DELETE':
    need = Need.objects.filter(client_id = client_id, pk=pk).first()
    need.delete()
    return JsonResponse({}, status=200)

@csrf_exempt
def need_resource(request, need_id, pk):
  if request.method == 'POST': # create NeedResourceMatch or update if one already exists for need / resource combination
    body_unicode = request.body.decode('utf-8')
    params = loads(body_unicode)

    NeedResourceMatch.objects.update_or_create(need_id = need_id, resource_id = pk,
      defaults={'pending': params['pending'], 'fulfilled': params['fulfilled']})

  elif request.method == 'DELETE':
    NeedResourceMatch.objects.filter(need_id = need_id, resource_id=pk).delete()

  need = Need.objects.get(pk=need_id)
  serializer = NeedResourceMatchStatusSerializer(need)
  return JsonResponse(serializer.data, safe=False)

class ClientDetail(APIView):
  def get_object(self, pk):
      try:
        return Client.objects.get(pk=pk)
      except Client.DoesNotExist:
        raise Http404

  def get(self, request, pk, format=None):
    client = self.get_object(pk)
    serializer = ClientSerializer(client)
    return JsonResponse(serializer.data)

  def put(self, request, pk, format=None):
    client = self.get_object(pk)
    serializer = ClientSerializer(client, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    client = self.get_object(pk)
    client.delete()
    return JsonResponse(status=status.HTTP_204_NO_CONTENT)

class ClientList(APIView):
  def get(self, request, format=None):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)

  def post(self, request, format=None):
    serializer = ClientSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)