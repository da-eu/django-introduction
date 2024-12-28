from django_filters import rest_framework as filters
from forum.models import Comment

class CommentFilter(filters.FilterSet):
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    max_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['min_id', 'max_id']