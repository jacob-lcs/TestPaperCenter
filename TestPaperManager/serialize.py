from rest_framework import serializers
from .models import *


class PaperSerialize(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = "__all__"


class TypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = QuestionTypes
        fields = "__all__"  


class DifficultySerialize(serializers.ModelSerializer):
    class Meta:
        model = QuestionDifficulty
        fields = "__all__"


class KnowledgePointSerialize(serializers.ModelSerializer):
    class Meta:
        model = KnowledgePoint
        fields = "__all__"


class QuestionSerialize(serializers.ModelSerializer):
    knowledge_point = KnowledgePointSerialize(many=True)
    type = TypeSerialize
    difficulty = DifficultySerialize
    paper_name = PaperSerialize

    class Meta:
        model = Question
        fields = "__all__"
