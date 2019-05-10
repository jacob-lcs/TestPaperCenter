from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import User, Paper, QuestionDifficulty, QuestionTypes, KnowledgePoint, Grade, Subject, School, Paper, \
    Question
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
    # 递归查询
    def search_children(a, b):
        if len(a.children.all()) != 0:
            ii = 0
            for i in a.children.all():
                if 'children' not in b.keys():
                    b['children'] = []
                b['children'].append({
                    'value': i.name,
                    'label': i.name
                })
                search_children(i, b['children'][ii])
                ii += 1

    response = []
    knowledgepoints = KnowledgePoint.objects.filter(parent=None)
    i = 0
    for knowledgepoint in knowledgepoints:
        a = {
            'value': knowledgepoint.name,
            'label': knowledgepoint.name
        }
        response.append(a)
        search_children(knowledgepoint, response[i])
        i += 1
    return JsonResponse(response, safe=False)


# 查询年级列表接口
@require_http_methods(["GET"])
def query_grades(request):
    response = []
    grades = Grade.objects.all()
    for grade in grades:
        response.append(model_to_dict(grade))
    return JsonResponse(response, safe=False)


# 查询科目列表接口
@require_http_methods(["GET"])
def query_subjects(request):
    response = []
    subjects = Subject.objects.all()
    for subject in subjects:
        response.append(model_to_dict(subject))
    return JsonResponse(response, safe=False)


# 保存单选题接口
@require_http_methods(['GET'])
def save_single_topic_selection(request):
    print(request.GET)
    school_name = request.GET.get('school_name')
    paper_name = request.GET.get('paper_name')
    paper_year = request.GET.get('paper_year')
    grade = request.GET.get('grade')
    subject = request.GET.get('subject')
    question_type = request.GET.get('question_type')
    question_stem = request.GET.get('question_stem')
    question_answer = request.GET.get('question_answer')
    question_difficult = request.GET.get('question_difficult')
    question_knowledgepoints = dict(request.GET).get('question_knowledgepoints[list][]')
    sql_school_name = School.objects.filter(name=school_name)
    if not sql_school_name:
        School(name=school_name).save()
    sql_school_name = School.objects.filter(name=school_name)
    sql_subject_name = Subject.objects.filter(name=subject)
    sql_grade = Grade.objects.filter(name=grade)
    sql_paper_name = Paper.objects.filter(name=paper_name, year=paper_year, subject_name_id=sql_subject_name.first().id,
                                          grade_id=sql_grade.first().id, school_name_id=sql_school_name.first().id)
    if not sql_paper_name:
        Paper(name=paper_name, year=paper_year, subject_name_id=sql_subject_name.first().id,
              grade_id=sql_grade.first().id, school_name_id=sql_school_name.first().id).save()
    sql_paper_name = Paper.objects.filter(name=paper_name)
    sql_question_type = QuestionTypes.objects.filter(name=question_type)
    sql_question_difficult = QuestionDifficulty.objects.filter(name=question_difficult)
    paper = Question.objects.create(stem=question_stem, answer=question_answer, type_id=sql_question_type.first().id,
                                    difficulty_id=sql_question_difficult.first().id,
                                    paper_name_id=sql_paper_name.first().id)
    knowledgepoints = []
    for knowledgepoint in question_knowledgepoints:
        knowledgepoints.append(KnowledgePoint.objects.filter(name=knowledgepoint).first().id)
    for k in knowledgepoints:
        paper.knowledge_point.add(k)
    response = {"res": "success"}
    return JsonResponse(response, safe=False)
