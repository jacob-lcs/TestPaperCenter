from django.contrib import admin
from .models import Grade
from .models import KnowledgePoint
from .models import Question
from .models import QuestionDifficulty
from .models import QuestionTypes
from .models import School
from .models import Subject
from .models import User


# Register your models here.
admin.site.register(Grade)
admin.site.register(KnowledgePoint)
admin.site.register(Question)
admin.site.register(QuestionDifficulty)
admin.site.register(QuestionTypes)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(User)
