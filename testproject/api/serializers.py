from rest_framework import serializers
from forum.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'date']
        read_only_fields = ['user']