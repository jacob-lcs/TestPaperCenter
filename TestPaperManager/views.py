from django.http import JsonResponse, FileResponse
import pyexcel_xlsx
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import User, Paper, QuestionDifficulty, QuestionTypes, KnowledgePoint, Grade, Subject, School, Paper, \
    Question
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json


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


# 查询知识点列表接口,递归形式
@require_http_methods(['GET'])
def query_knowledgepoint(request):
    subject = request.GET.get('subject')
    subject_id = Subject.objects.filter(name=subject).first().id

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
    knowledgepoints = KnowledgePoint.objects.filter(parent=None, subject_name_id=subject_id)
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


# 查询知识点列表接口，非递归形式
@require_http_methods(["GET"])
def query_knowledge_point_list(request):
    response = []
    subject = request.GET.get("subject")
    subject_id = Subject.objects.filter(name=subject).first().id
    KnowledgePoint_list = KnowledgePoint.objects.filter(subject_name_id=subject_id)
    for knowledge in KnowledgePoint_list:
        response.append(model_to_dict(knowledge))
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
    if not Question.objects.filter(stem=question_stem, answer=question_answer):
        if not sql_school_name:
            School(name=school_name).save()
        sql_school_name = School.objects.filter(name=school_name)
        sql_subject_name = Subject.objects.filter(name=subject)
        sql_grade = Grade.objects.filter(name=grade)
        sql_paper_name = Paper.objects.filter(name=paper_name, year=paper_year,
                                              subject_name_id=sql_subject_name.first().id,
                                              grade_id=sql_grade.first().id, school_name_id=sql_school_name.first().id)
        if not sql_paper_name:
            Paper(name=paper_name, year=paper_year, subject_name_id=sql_subject_name.first().id,
                  grade_id=sql_grade.first().id, school_name_id=sql_school_name.first().id).save()
        sql_paper_name = Paper.objects.filter(name=paper_name)
        sql_question_type = QuestionTypes.objects.filter(name=question_type)
        sql_question_difficult = QuestionDifficulty.objects.filter(name=question_difficult)
        paper = Question.objects.create(stem=question_stem, answer=question_answer,
                                        type_id=sql_question_type.first().id,
                                        difficulty_id=sql_question_difficult.first().id,
                                        paper_name_id=sql_paper_name.first().id)
        knowledgepoints = []
        for knowledgepoint in question_knowledgepoints:
            knowledgepoints.append(KnowledgePoint.objects.filter(name=knowledgepoint).first().id)
        for k in knowledgepoints:
            paper.knowledge_point.add(k)
    response = {"res": "success"}
    return JsonResponse(response, safe=False)


# 添加知识点接口
@require_http_methods(["GET"])
def add_knowledge_points(request):
    child_knowledge_point = request.GET.get("child_knowledge_point")
    parent_knowledge_point = request.GET.get("parent_knowledge_point")
    subject = request.GET.get("subject")
    if parent_knowledge_point != '':
        parent_id = KnowledgePoint.objects.filter(name=parent_knowledge_point).first().id
    else:
        parent_id = None
    subject_id = Subject.objects.filter(name=subject).first().id
    KnowledgePoint.objects.create(name=child_knowledge_point, parent_id=parent_id, subject_name_id=subject_id)
    return JsonResponse({"res": "success"}, safe=False)


# 查询页面的数据数量
@require_http_methods(["GET"])
def query_data_count(request):
    count = len(Question.objects.all())
    return JsonResponse({"count": count}, safe=False)


# 查询页面的指定数据
@require_http_methods(["GET"])
def query_question_data(request):
    response = []
    start = int(request.GET.get("start"))
    page_count = int(request.GET.get("page_count"))
    start = (start - 1) * page_count
    qs = Question.objects.all().order_by('-id')[start:(start + page_count)]
    for q in qs:
        a = {"question_content": q.stem, "question_answer": q.answer, "question_type": q.type.name,
             "question_difficulty": q.difficulty.name, "paper_name": q.paper_name.name}
        response.append(a)
    return JsonResponse(response, safe=False)


# 删除指定题目
@require_http_methods(["GET"])
def delete_question(request):
    question_content = request.GET.get("question_content")
    question_answer = request.GET.get("question_answer")
    question_type = request.GET.get("question_type")
    question_difficulty = request.GET.get("question_difficulty")
    paper_name = request.GET.get("paper_name")
    Question.objects.filter(stem=question_content, answer=question_answer, type__name=question_type,
                            difficulty__name=question_difficulty, paper_name__name=paper_name).delete()
    return JsonResponse({"res": "success"}, safe=False)


# 上传
@csrf_exempt
def upload_excel(request):
    if request.method == "POST":
        file = request.FILES['file']
        error_time = 0
        formatted_excel_data = list(pyexcel_xlsx.get_data(file).values())[0]
        for i in range(2, len(formatted_excel_data)):
            if '' in formatted_excel_data[i][0:9] or formatted_excel_data[i] == []:
                error_time += 1
                continue
            else:
                school_name = formatted_excel_data[i][9]
                paper_name = formatted_excel_data[i][5]
                paper_year = formatted_excel_data[i][6]
                grade = formatted_excel_data[i][8]
                subject = formatted_excel_data[i][7]
                question_type = formatted_excel_data[i][2]
                question_stem = formatted_excel_data[i][0]
                question_answer = formatted_excel_data[i][1]
                question_difficult = formatted_excel_data[i][3]
                question_knowledgepoints = formatted_excel_data[i][4].split('；')
                sql_school_name = School.objects.filter(name=school_name)
                if not Question.objects.filter(stem=question_stem, answer=question_answer):
                    if not sql_school_name:
                        School(name=school_name).save()
                    sql_school_name = School.objects.filter(name=school_name)
                    sql_subject_name = Subject.objects.filter(name=subject)
                    sql_grade = Grade.objects.filter(name=grade)
                    sql_paper_name = Paper.objects.filter(name=paper_name, year=paper_year,
                                                          subject_name_id=sql_subject_name.first().id,
                                                          grade_id=sql_grade.first().id,
                                                          school_name_id=sql_school_name.first().id)
                    if not sql_paper_name:
                        Paper(name=paper_name, year=paper_year, subject_name_id=sql_subject_name.first().id,
                              grade_id=sql_grade.first().id, school_name_id=sql_school_name.first().id).save()
                    sql_paper_name = Paper.objects.filter(name=paper_name)
                    sql_question_type = QuestionTypes.objects.filter(name=question_type)
                    sql_question_difficult = QuestionDifficulty.objects.filter(name=question_difficult)
                    paper = Question.objects.create(stem=question_stem, answer=question_answer,
                                                    type_id=sql_question_type.first().id,
                                                    difficulty_id=sql_question_difficult.first().id,
                                                    paper_name_id=sql_paper_name.first().id)
                    knowledgepoints = []
                    print(question_knowledgepoints)
                    for knowledgepoint in question_knowledgepoints:
                        knowledgepoints.append(KnowledgePoint.objects.filter(name=knowledgepoint).first().id)
                    for k in knowledgepoints:
                        paper.knowledge_point.add(k)
        response = {"res": "success"}
        return JsonResponse(response, safe=False)


@csrf_exempt
def search_questions(request):
    if request.method == 'POST':
        print(json.loads(request.body.decode()))
    return JsonResponse({'ok': True})
