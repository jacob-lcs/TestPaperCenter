from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import User


@require_http_methods(["GET"])
def login(request):
    response = {}
    name = request.GET.get('name')
    password = request.GET.get('psw')
    res = User.objects.filter(name=name, password=password)
    if res:
        identity = res.first().identity
        response = {'res': 'yes', 'identity': identity}
    else:
        response = {'res': 'no'}
    return JsonResponse(response)
