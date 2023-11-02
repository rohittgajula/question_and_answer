from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer


@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password'])
            )
            return Response({
                'details':'User registered.'
            }, status.HTTP_201_CREATED)
        else:
            return Response({
                'error':'User already exists.'
            }, status.HTTP_404_NOT_FOUND)
    return Response(user.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = SignUpSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_user(request):
    queryset = User.objects.all().order_by('id')
    serializer = UserSerializer(queryset, many=True)
    return Response({
        'Authors':serializer.data
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    data = request.data
    author = request.user

    author.first_name = data['first_name']
    author.last_name = data['last_name']
    author.email = data['email']
    author.username = data['email']
    if data['password'] != "":
        author.password = make_password(data['passowrd'])
    author.save()

    serializer = UserSerializer(author, many=False)
    return Response({
        'updated data':serializer.data
    }, status.HTTP_202_ACCEPTED)

