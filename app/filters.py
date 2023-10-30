from django_filters import rest_framework as filters
from .models import Question, Answer

class QuestionFilters(filters.FilterSet):

    question = filters.CharFilter(field_name='question', lookup_expr='icontains')
    tag = filters.CharFilter(field_name='tag', lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ('question', 'tag')

        