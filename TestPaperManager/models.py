from django.db import models


# Create your models here.
class User(models.Model):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    name = models.CharField('用户名', max_length=200)
    password = models.CharField('密码', max_length=200)
    identity = models.CharField('身份', max_length=200)

    def __str__(self):
        return self.name


class School(models.Model):
    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name

    name = models.CharField('学校名称', max_length=200)

    def __str__(self):
        return self.name


class QuestionTypes(models.Model):
    class Meta:
        verbose_name = '题目类型'
        verbose_name_plural = verbose_name

    name = models.CharField('题目类型', max_length=200)

    def __str__(self):
        return self.name


class QuestionDifficulty(models.Model):
    class Meta:
        verbose_name = '题目难度'
        verbose_name_plural = verbose_name

    name = models.CharField('题目难度', max_length=200)

    def __str__(self):
        return self.name


class Subject(models.Model):
    class Meta:
        verbose_name = '科目'
        verbose_name_plural = verbose_name

    name = models.CharField('科目名称', max_length=200)

    def __str__(self):
        return self.name


class Grade(models.Model):
    class Meta:
        verbose_name = '年级'
        verbose_name_plural = verbose_name

    name = models.CharField('年级', max_length=200)

    def __str__(self):
        return self.name


class Paper(models.Model):
    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

    name = models.CharField('试卷名称', max_length=200)
    year = models.CharField('试卷年份', max_length=200)

    def __str__(self):
        return self.name


class KnowledgePoint(models.Model):
    class Meta:
        verbose_name = '知识点'
        verbose_name_plural = verbose_name

    name = models.CharField('知识点', max_length=200)
    subject_name = models.ForeignKey(to='Subject', on_delete=models.CASCADE, verbose_name='科目名称')
    parent = models.ForeignKey(to='KnowledgePoint', on_delete=models.CASCADE, verbose_name='上级知识点', null=True,
                               blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name

    stem = models.CharField('题干', max_length=2000)
    answer = models.CharField('答案', max_length=1000)
    type = models.ForeignKey(to='QuestionTypes', on_delete=models.CASCADE, verbose_name='题目类型')
    difficulty = models.ForeignKey(to='QuestionDifficulty', on_delete=models.CASCADE, verbose_name='题目难度')
    school_name = models.ForeignKey(to='School', on_delete=models.CASCADE, verbose_name='学校名称')
    subject_name = models.ForeignKey(to='Subject', on_delete=models.CASCADE, verbose_name='学科名称')
    grade = models.ForeignKey(to='Grade', on_delete=models.CASCADE, verbose_name='年级名称')
    paper_name = models.ForeignKey(to='Paper', on_delete=models.CASCADE, verbose_name='试卷名称')
    knowledge_point = models.ManyToManyField(to='KnowledgePoint', related_name='question', verbose_name='知识点')

    def __str__(self):
        return self.stem
