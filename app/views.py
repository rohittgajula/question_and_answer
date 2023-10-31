from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Question, Answer, upVote, downVote
from .serializers import QuestionSerializer, AnswerSerializer, upVoteSerailizer
from .filters import QuestionFilters

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    filterser = QuestionFilters(request.GET, queryset=Question.objects.all().order_by('id'))

    serializer = QuestionSerializer(filterser.qs, many=True)
    return Response({
        'Questions':serializer.data
    }, status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_question(request):
    data = request.data
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
        question = Question.objects.create(**data, author=request.user)
        que = QuestionSerializer(question, many=False)
        return Response({
            'details':que.data
        }, status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_question(request, pk):
    question = get_object_or_404(Question, id=pk)
    serializer = QuestionSerializer(question, many=False)
    return Response({
        'question':serializer.data
    }, status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_question(request, pk):
    data = request.data
    question = get_object_or_404(Question, id=pk)

    if question.author != request.user:
        return Response({
            'error':'you cannot update this question.'
        }, status.HTTP_401_UNAUTHORIZED)

    question.question = data['question']
    question.tag = data['tag']

    question.save()
    serializer = QuestionSerializer(question, many=False)
    return Response({
        'updated question':serializer.data
    }, status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_question(request, pk):
    question = get_object_or_404(Question, id=pk)

    if question.author != request.user:
        return Response({
            'error':'you cannot delete this question.'
        })

    question.delete()
    return Response({
        'details':'Sucessfully Deleated.'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_answer(request, pk):
    author = request.user
    data = request.data
    question = get_object_or_404(Question, id=pk)

    answer = question.answers.filter(author=author)

    if answer.exists():
        new_answer = {
            'answer':data['answer']
        }
        answer.upadte(**new_answer)
        return Response({
            'details':'Answer Updated'
        }, status.HTTP_202_ACCEPTED)
    else:
        Answer.objects.create(
            author=author,
            question=question,
            answer = data['answer']
        )
        return Response({
            'details':'Answer Created.',
        }, status.HTTP_201_CREATED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_answer(request, pk):
    author = request.user
    question = get_object_or_404(Question, id=pk)
    answer = question.answers.filter(author=author)
    if answer.exists():
        answer.delete()
        return Response({
            'details':'Deleated sucessfully.'
        }, status.HTTP_200_OK)
    else:
        return Response({
            'error':'Does not exist.'
        }, status.HTTP_404_NOT_FOUND)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote(request, pk):
    answer = get_object_or_404(Answer, id=pk)
    author=request.user
    voter = upVote.objects.filter(author=author, answer=answer)        # answer_id=pk
    if voter.exists():
        return Response({
            'details':'You cannot vote twice'
        })
    else:
        upVote.objects.create(
            answer=answer,
            author=author
        )
        answer.upVotes += 1
        answer.save()
        return Response({
            'details':'Vote added'
        })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote(request, pk):
    answer = get_object_or_404(Answer, id=pk)
    author = request.user
    voter = downVote.objects.filter(author=author, answer=answer)
    if voter.exists():
        return Response({
            'error':'You cannot vote twice.'
        })
    else:
        downVote.objects.create(
            answer=answer,
            author=author
        )
        answer.downVotes -= 1
        answer.save()
        return Response({
            'details':'downvote added'
        })


