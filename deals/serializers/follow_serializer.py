from rest_framework import serializers
from ..models import Follow

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source='follower.username')
    following_username = serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_username','following', 'following_username', 'created_at']
        read_only_fields = ['follower', 'created_at']