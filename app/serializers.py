from rest_framework import serializers
from .models import Question, Answer, upVote, downVote

class AnswerSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField(method_name='get_votes', read_only=True)
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'author', 'createdAt', 'votes')

    def get_votes(self, obj):
        total_votes = 0
        if obj.upVotes is not None and obj.downVotes is not None:
            total_votes = (obj.upVotes + obj.downVotes)
            print(total_votes)
            return total_votes       

class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField(method_name='get_answers', read_only = True)
    class Meta:
        model = Question
        fields = ('id', 'author', 'question', 'answer', 'tag', 'createdAt')
    def get_answers(self, obj):
        answers = obj.answers.all()
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data

class upVoteSerailizer(serializers.ModelSerializer):
    class Meta:
        model = upVote
        fields = '__all__'

class downVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = downVote
        fields = '__all__'

