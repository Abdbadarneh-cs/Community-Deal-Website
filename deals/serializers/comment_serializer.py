from rest_framework import serializers
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'deal', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']