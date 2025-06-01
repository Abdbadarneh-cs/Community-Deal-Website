# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from deals.models import Follow
# from ..serializers import FollowSerializer
# from django.contrib.auth import get_user_model
# from ..serializers import follow_serializer
# User = get_user_model()

# class FollowUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         following = get_object_or_404(User, id=user_id)
#         if following == request.user:
#             return Response({'detail': "Can't follow yourself"}, status=400)
#         follow, created = Follow.objects.get_or_create(follower=request.user, following=following)
#         if not created:
#             return Response({'detail': 'Already following'}, status=400)
#         return Response(FollowSerializer(follow).data, status=201)

# class UnfollowUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, user_id):
#         follow = Follow.objects.filter(follower=request.user, following_id=user_id).first()
#         if follow:
#             follow.delete()
#             return Response({'detail': 'Unfollowed'}, status=204)
#         return Response({'detail': 'Not following'}, status=400)