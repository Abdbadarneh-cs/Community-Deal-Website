from rest_framework import serializers
from ..models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'deal', 'created_at']
        read_only_fields = ['user', 'created_at']