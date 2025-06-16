from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from deals.models import Like, Deal
from django.shortcuts import get_object_or_404
from ..serializers import like_serializer
class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, deal_id):
        deal = get_object_or_404(Deal, id=deal_id)
        like, created = Like.objects.get_or_create(user=request.user, deal=deal)
        if not created:
            like.delete()
            return Response({'liked': False})
        return Response({'liked': True})