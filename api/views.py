from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from json import loads
from api.models import *
from api.serializers import *
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
def clients(request):
  if request.method == 'GET':
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def dashboard_clients(request):
  if request.method == 'GET':
    clients = Client.objects.all()
    serializer = DashboardClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def client(request, pk):
  if request.method == 'GET':
    client = Client.objects.get(pk=pk)
    serializer = ClientSerializer(client)
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

# need = Need.objects.filter(client_id = client_id, pk=pk)
# if need:
#   return HttpResponse("<h5>if</h5>")

# data = JSONParser().parse(request
# serializer = NeedSerializer(data=data)

# if serializer.is_valid():
#     serializer.save()
#     return JsonResponse(serializer.data, status=201)
# return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def resources(request):
#     if request.method == 'GET':
#       params = loads(request.GET.get('params', '{}'))
      
#       q_objects = Q()
#       for param_name, value in params['details'].items():
#         q_objects.add(Q(**{'{0}__{1}'.format('details', param_name): value}), Q.AND)

#       resources = Resource.objects.filter(type=params['type']).filter(q_objects)
#       serializer = ResourceSerializer(resources, many=True)
#       return JsonResponse(serializer.data, safe=False)

# elif request.method == 'POST':
#     data = JSONParser().parse(request)
#     serializer = ResourceSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data, status=201)
#     return JsonResponse(serializer.errors, status=400)
