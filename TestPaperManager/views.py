from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import User, Paper, QuestionDifficulty, QuestionTypes, KnowledgePoint
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict


# 登录接口
@require_http_methods(["GET"])
def login(request):
    response = {}
    name = request.GET.get('name')
    password = request.GET.get('psw')
    res = User.objects.filter(name=name)
    pas = res.first().password
    print(pas)
    ress = check_password(password, pas)
    if ress:
        identity = res.first().identity
        response = {'res': 'yes', 'identity': identity}
    else:
        response = {'res': 'no'}
    return JsonResponse(response)


# 添加试卷接口
@require_http_methods(["GET"])
def add_paper(request):
    paper_name = request.GET.get('paper_name')
    paper_year = request.GET.get('paper_year')
    paper_subject = request.GET.get('paper_subject')

    Paper(name=paper_name, year=paper_year, subject=paper_subject).save()
    response = {'res': 'yes'}
    return JsonResponse(response, safe=False)


# 查询题目难度接口
@require_http_methods(["GET"])
def query_difficulty(request):
    response = []
    Difficulties = QuestionDifficulty.objects.all()
    for Difficulty in Difficulties:
        response.append(model_to_dict(Difficulty))
    return JsonResponse(response, safe=False)


# 查询题目类型接口
@require_http_methods(["GET"])
def query_types(request):
    response = []
    types = QuestionTypes.objects.all()
    for type in types:
        response.append(model_to_dict(type))
    return JsonResponse(response, safe=False)


# 查询知识点列表接口
@require_http_methods(['GET'])
def query_knowledgepoint(request):
    response = []
    knowledgepoints = KnowledgePoint.objects.all()
    for knowledgepoint in knowledgepoints:
        response.append(model_to_dict(knowledgepoint))
    return JsonResponse(response, safe=False)