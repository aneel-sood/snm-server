from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from json import loads
from api.models import *
from api.serializers import *
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from rest_framework_csv import renderers as csv_renderers

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
    return Response(status=status.HTTP_204_NO_CONTENT)

class ClientList(APIView):
  renderer_classes = (csv_renderers.CSVRenderer, )

  def get_renderer_context(self):
    context = super().get_renderer_context()
    context['header'] = ['id', 'first_name', 'last_name', 'birthdate', 
      'email', 'cell_phone', 'home_phone', 'location', 
      'needs_without_matching_resources_count',
      'needs_with_matching_resources_count', 'pending_needs_count', 
      'fulfilled_needs_count', 'most_recent_match_activity_datetime']
    context['labels'] = {'location': 'address'}
    return context

  def get(self, request, format=None):
    clients = Client.objects.all()
    if format == 'csv':
      serializer = ClientCSVSerializer(clients, many=True)
      return Response(serializer.data)
    else:
      serializer = ClientSerializer(clients, many=True)
      return JsonResponse(serializer.data, safe=False)

  def post(self, request, format=None):
    serializer = ClientSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProviderDetail(APIView):
  def get_object(self, pk):
      try:
        return Provider.objects.get(pk=pk)
      except Provider.DoesNotExist:
        raise Http404

  def get(self, request, pk, format=None):
    provider = self.get_object(pk)
    serializer = ProviderSerializer(provider)
    return JsonResponse(serializer.data)

  def put(self, request, pk, format=None):
    provider = self.get_object(pk)
    serializer = ProviderSerializer(provider, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    provider = self.get_object(pk)
    provider.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ProviderList(APIView):
  def get(self, request, format=None):
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers, many=True)
    return JsonResponse(serializer.data, safe=False)
      
  def post(self, request, format=None):
    serializer = ProviderSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NeedList(APIView):
  renderer_classes = (csv_renderers.CSVRenderer, )

  def get_renderer_context(self):
    context = super().get_renderer_context()
    context['header'] = ['client_id', 'type', 'matching_resources_count',
      'pending_resources_count', 'fulfilled_resources_count', 'created_at']
    return context

  def get(self, request, format=None):
    needs = Need.objects.all()
    if format == 'csv':
      serializer = NeedCSVSerializer(needs, many=True)
      return Response(serializer.data)
    else:
      serializer = NeedSerializer(needs, many=True)
      return JsonResponse(serializer.data, safe=False)
