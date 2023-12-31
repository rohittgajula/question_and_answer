from django.urls import path
from . import views

urlpatterns = [
    # questions
    path('questions/', views.get_questions, name='get_questions'),
    path('questions/new/', views.new_question, name='new_question'),
    path('questions/<str:pk>/', views.single_question, name='single_question'),
    path('questions/<str:pk>/update/', views.update_question, name='update_question'),
    path('questions/<str:pk>/delete/', views.delete_question, name='delete_question'),

    # answers
    path('<str:pk>/answer/', views.create_answer, name='create_answer'),
    path('<str:pk>/answer/delete/', views.delete_answer, name='delete_answer'), # questions related answers will be deleated. here pk is ID of question.

    # votings
    path('answer/<str:pk>/upvote/', views.upvote, name='upvote'),
    path('answer/<str:pk>/downvote/', views.downvote, name='downvote'),
]

