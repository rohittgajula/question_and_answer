from django.db import models
from django.contrib.auth.models import User

class Tag(models.TextChoices):
    NONE = 'None'
    DJANGO = 'Django'
    PYTHON = 'Python'
    DJANGO_REST_FRAMEWORK = 'Django_rest_framework'
    JAVA = 'Java'
    JAVASCRIPT = 'JavaScript'
    PHP = 'PHP'
    POSTGRES = 'Postgres'
    MYSQL = 'MySql'
    AWS = 'AWS'

class Question(models.Model):
    question = models.CharField(max_length=250, default="", blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=50, choices=Tag.choices, default="NONE", blank=True)

    def __str__(self):
        return str(self.question)
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=1000, default="", blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.answer)
    
