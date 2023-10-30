from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'votes', 'author', 'createdAt')

class QuestionSerializer(serializers.ModelSerializer):

    answer = serializers.SerializerMethodField(method_name='get_answers', read_only = True)

    class Meta:
        model = Question
        fields = ('id', 'author', 'question', 'answer', 'tag', 'createdAt')

    def get_answers(self, obj):
        answers = obj.answers.all()
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data


