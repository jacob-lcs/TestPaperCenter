from django.contrib import admin
from .models import Grade
from .models import KnowledgePoint
from .models import Question
from .models import QuestionDifficulty
from .models import QuestionTypes
from .models import School
from .models import Subject
from .models import User
from .models import Paper


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(KnowledgePoint)
class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'parent']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'stem', 'answer', 'type', 'difficulty',  'paper']
    pass


@admin.register(QuestionDifficulty)
class QuestionDifficultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    pass


@admin.register(QuestionTypes)
class QuestionTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'password', 'identity']


@admin.register(Paper)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'subject', 'grade', 'school']
