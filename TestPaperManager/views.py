import json
import numpy.random
import os, zipfile

import pyexcel_xlsx
import pypandoc
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import User, QuestionDifficulty, QuestionTypes, KnowledgePoint, Grade, Subject, School, Paper, \
    Question, Img
from .serialize import QuestionSerialize

STATIC_PATH = r"TestPaperManager/static/TestPaperManager/"
CHINESE_NUMBER = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']


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
    subject = request.GET.get('subject')
    if request.GET.get('id', False):
        types = QuestionTypes.objects.filter(subject_id=subject)
    else:
        types = QuestionTypes.objects.filter(subject__name=subject)

    for type in types:
        response.append(model_to_dict(type))
    return JsonResponse(response, safe=False)


# 查询知识点列表接口,递归形式
@require_http_methods(['GET'])
def query_knowledgepoint(request):
    subject = request.GET.get('subject')

    if request.GET.get('id', False):
        subject_id = int(subject)
    else:
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
    knowledgepoints = KnowledgePoint.objects.filter(parent=None, subject_id=subject_id)
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
    KnowledgePoint_list = KnowledgePoint.objects.filter(subject_id=subject_id)
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


# 保存题目接口
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
    question_options = request.GET.get('question_options')
    question_knowledgepoints = dict(request.GET).get('question_knowledgepoints[list][]')
    sql_school_name = School.objects.filter(name=school_name)
    print(paper_name)
    if not Question.objects.filter(stem=question_stem, answer=question_answer, paper__name=paper_name):
        print(paper_name)
        if not sql_school_name:
            School(name=school_name).save()
        sql_school_name = School.objects.filter(name=school_name)
        sql_subject_name = Subject.objects.filter(name=subject)
        sql_grade = Grade.objects.filter(name=grade)
        sql_paper_name = Paper.objects.filter(name=paper_name, year=paper_year,
                                              subject_id=sql_subject_name.first().id,
                                              grade_id=sql_grade.first().id, school_id=sql_school_name.first().id)
        if not sql_paper_name:
            Paper(name=paper_name, year=paper_year, subject_id=sql_subject_name.first().id,
                  grade_id=sql_grade.first().id, school_id=sql_school_name.first().id).save()
        sql_paper_name = Paper.objects.filter(name=paper_name)
        sql_question_type = QuestionTypes.objects.filter(name=question_type, subject__name=subject)
        sql_question_difficult = QuestionDifficulty.objects.filter(name=question_difficult)
        paper = Question.objects.create(stem=question_stem, answer=question_answer,
                                        type_id=sql_question_type.first().id,
                                        difficulty_id=sql_question_difficult.first().id,
                                        paper_id=sql_paper_name.first().id, options=question_options)
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
    KnowledgePoint.objects.create(name=child_knowledge_point, parent_id=parent_id, subject_id=subject_id)
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
        a = {"id": q.id, "question_content": q.stem, "question_answer": q.answer, "question_type": q.type.name,
             "question_difficulty": q.difficulty.name, "paper_name": q.paper.name, "question_options": q.options}
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
                            difficulty__name=question_difficulty, paper__name=paper_name).delete()
    return JsonResponse({"res": "success"}, safe=False)


# 上传
@csrf_exempt
def upload_excel(request):
    if request.method == "POST":
        file = request.FILES['file']
        error_time = 0
        formatted_excel_data = list(pyexcel_xlsx.get_data(file).values())[0]
        for i in range(1, len(formatted_excel_data)):
            if '' in formatted_excel_data[i][0:9] or formatted_excel_data[i] == []:
                error_time += 1
                continue
            else:
                school_name = formatted_excel_data[i][7]
                paper_name = formatted_excel_data[i][4]
                paper_year = formatted_excel_data[i][5]
                grade = formatted_excel_data[i][6]
                subject = formatted_excel_data[i][0]
                question_type = formatted_excel_data[i][1]
                question_stem = formatted_excel_data[i][8]
                question_answer = formatted_excel_data[i][9]
                question_difficult = formatted_excel_data[i][2]
                question_knowledgepoints = formatted_excel_data[i][3].split('；')
                sql_school_name = School.objects.filter(name=school_name)
                question_options = ''
                for ii in range(10, len(formatted_excel_data[i])):
                    question_options += formatted_excel_data[i][ii] + "\n"
                if not Question.objects.filter(stem=question_stem, answer=question_answer, paper__name=paper_name):
                    if not sql_school_name:
                        School(name=school_name).save()
                    sql_school_name = School.objects.filter(name=school_name)
                    sql_subject_name = Subject.objects.filter(name=subject)
                    sql_grade = Grade.objects.filter(name=grade)
                    sql_paper_name = Paper.objects.filter(name=paper_name, year=paper_year,
                                                          subject_id=sql_subject_name.first().id,
                                                          grade_id=sql_grade.first().id,
                                                          school_id=sql_school_name.first().id)
                    if not sql_paper_name:
                        Paper(name=paper_name, year=paper_year, subject_id=sql_subject_name.first().id,
                              grade_id=sql_grade.first().id, school_id=sql_school_name.first().id).save()
                    sql_paper_name = Paper.objects.filter(name=paper_name)
                    sql_question_type = QuestionTypes.objects.filter(name=question_type, subject__name=subject)
                    sql_question_difficult = QuestionDifficulty.objects.filter(name=question_difficult)
                    paper = Question.objects.create(stem=question_stem, answer=question_answer,
                                                    type_id=sql_question_type.first().id,
                                                    difficulty_id=sql_question_difficult.first().id,
                                                    paper_id=sql_paper_name.first().id, options=question_options)
                    knowledgepoints = []
                    print(question_knowledgepoints)
                    for knowledgepoint in question_knowledgepoints:
                        knowledgepoints.append(KnowledgePoint.objects.filter(name=knowledgepoint).first().id)
                    for k in knowledgepoints:
                        paper.knowledge_point.add(k)
        print(error_time)
        response = {"res": "success"}
        return JsonResponse(response, safe=False)


# 上传图片接口
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        img = Img(img_url=request.FILES['file'])
        img.save()
        print(str(img.img_url))
        return JsonResponse({'url': str(img.img_url)}, safe=False)


# 获取一道题的所有内容
@require_http_methods('GET')
def get_question_all_content(request):
    question_id = request.GET.get('question_id')
    print(question_id)
    question = Question.objects.filter(id=question_id)
    result = question.first()
    print(result)
    response = {"stem": result.stem, "answer": result.answer, "difficulty": result.difficulty.name,
                "paper": result.paper.name, "type": result.type.name, "options": result.options,
                "school": result.paper.school.name, "year": result.paper.year, "grade": result.paper.grade.name,
                "subject": result.paper.subject.name}
    return JsonResponse(response, safe=False)


# zlm's------------------------------------------------------------
@require_http_methods(["GET"])
def query_school(request):
    response = []
    schools = School.objects.all()
    for school in schools:
        response.append(model_to_dict(school))
    return JsonResponse(response, safe=False)


@csrf_exempt
def search_questions(request):
    if request.method == 'POST':
        response = {'ok': False}
        request_data = json.loads(request.body.decode())
        # 获取全部数据all
        isall = request_data.get('isall', False)
        if isall:
            response['ok'] = True
            response['data'] = QuestionSerialize(Question.objects.all(), many=True).data
        else:
            paperInfo = request_data.get('paperInfo', False)
            filters = request_data.get('filters', False)
            knowledge_point = request_data.get('knowledge_point', False)
            school_selected = request_data.get('school_selected', False)
            if paperInfo and paperInfo['ok']:
                print('paperInfo:', paperInfo)
                # print('filters[0]:', filters[0])  # 难度
                # print('filters[1]:', filters[1])  # 题型
                condion = Q()
                # 根据年级和科目筛选
                subject_id = paperInfo.get('subject')
                grade_id = paperInfo.get('grade')
                condion &= Q(paper__subject_id=subject_id)
                condion &= Q(paper__grade_id=grade_id)
                # 根据学校和知识点筛选
                print("knowledge_point", knowledge_point)
                print('school_selected', school_selected)
                if knowledge_point:
                    condion &= Q(knowledge_point__name__in=knowledge_point)
                if school_selected:
                    condion &= Q(paper__school__id__in=school_selected)
                # 根据难度和题型筛选
                difficulty = [i['id'] for i in filters[0]['items'] if not i['selected']]
                if difficulty:
                    print('难度：', difficulty)
                    condion &= Q(difficulty_id__in=difficulty)
                type = [i['id'] for i in filters[1]['items'] if not i['selected']]
                if type:
                    print('题型：', type)
                    condion &= Q(type_id__in=type)
                response['ok'] = True
                response['data'] = QuestionSerialize(Question.objects.filter(condion), many=True).data
                return JsonResponse(response, safe=False)
        return JsonResponse(response)
    return JsonResponse({'ok': False, 'errmsg': 'Only accept POST request'})


# 查询科目列表接口
@csrf_exempt
def paper_export(request):
    if request.method == 'POST':
        response = {'ok': False}
        request_data = json.loads(request.body.decode())
        randomKey = request_data.get('randomKey', False)
        questionSelected = request_data.get('questionSelected', False)
        print(questionSelected)
        for has_answer in [0, 1]:
            data_to_paper = ''
            # 大题号
            m = 0
            # 小题号
            n = 1
            for i, question in enumerate(questionSelected):
                # 这是stem
                if question['id'] > 0:
                    data_to_paper += str(n) + '、 ' + question['stem'] + '\n\n'
                    n += 1
                elif question['id'] < 0:
                    data_to_paper += CHINESE_NUMBER[m] + "、 " + question['stem'] + '\n\n'
                    m += 1
                else:
                    data_to_paper += question['stem'] + '\n\n'

                # 这是options
                data_to_paper += question['options'].replace('\n', '\n\n ') + '\n\n'
                if has_answer and question['id'] > 0:
                    data_to_paper += '答案： ' + question['answer'] + '\n\n'
            response = {'ok': True}
            if not os.path.exists(STATIC_PATH + r"docx/" + randomKey):
                os.mkdir(STATIC_PATH + r"docx/" + randomKey)
            if has_answer:
                md_to_docx(data_to_paper, randomKey + 'answer')
            else:
                md_to_docx(data_to_paper, randomKey)
            make_zip(STATIC_PATH + r"docx/" + randomKey + '/',
                     STATIC_PATH + r"zip/" + randomKey + '.zip')
        return JsonResponse(response)
    return JsonResponse({'ok': False, 'errmsg': 'Only accept POST request'})


# Tools
def md_to_docx(md_txt, filename):
    md_path = r"TestPaperManager/use_pandoc/temp.md"
    docx_path = r"TestPaperManager/static/TestPaperManager/docx/" + filename[:8] + '/' + filename + ".docx"

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_txt)
    pypandoc.convert_file(md_path, 'docx', outputfile=docx_path)


def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


@csrf_exempt
def auto_export(request):
    request_data = json.loads(request.body.decode())
    questionInfo = request_data.get('questionInfo', False)
    paperInfo = request_data.get('paperInfo', False)
    randomKey = request_data.get('randomKey', False)
    # randomKey = 'ASDS23F3'
    print(request_data)
    response = {'ok': True}
    for has_answer in [0, 1]:
        # 大题号
        m = 0
        # 小题号
        n = 1
        # 导出的markdown文本
        data_to_paper = "**" + paperInfo['paper_name'] + '**\n\n'
        for i in questionInfo:
            qs = Question.objects.filter(difficulty_id=i['difficulty'], type_id=i['type'])
            print(i, qs.count())
            if qs.count() < int(i['num']):
                response['ok'] = False
                response['errmsg'] = '题库里面的题目不够你导出哦，难度为%s的%s只有%d道哦！' % (
                    QuestionDifficulty.objects.get(id=i['difficulty']).name,
                    QuestionTypes.objects.get(id=i['type']),
                    qs.count()
                )
                return JsonResponse(response)
            else:
                response['ok'] = True
                # 加入题型标签
                data_to_paper += CHINESE_NUMBER[m] + "、 " + QuestionTypes.objects.get(id=i['type']).name + '\n\n'
                m += 1
                # 加入题目
                for j in numpy.random.choice(qs, size=i['num'], replace=False):
                    data_to_paper += str(n) + '、 ' + j.stem + '\n\n'
                    data_to_paper += j.options.replace('\n', '\n\n') + '\n\n'
                    n += 1
                    if has_answer:
                        data_to_paper += '答案： ' + j.answer + '\n\n'
        if not os.path.exists(STATIC_PATH + r"docx/" + randomKey):
            os.mkdir(STATIC_PATH + r"docx/" + randomKey)
        if has_answer:
            md_to_docx(data_to_paper, randomKey + 'answer')
        else:
            md_to_docx(data_to_paper, randomKey)
        make_zip(STATIC_PATH + r"docx/" + randomKey + '/',
                 STATIC_PATH + r"zip/" + randomKey + '.zip')
    return JsonResponse(response)
