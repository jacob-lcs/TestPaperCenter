from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def test(request):
    response = {'res': 'ok'}
    return JsonResponse(response)
