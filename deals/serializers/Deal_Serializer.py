from rest_framework import serializers
from ..models import Deal

class DealSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Deal
        fields = '__all__'