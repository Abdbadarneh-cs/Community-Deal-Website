from rest_framework import generics, permissions ,status
from .models import Deal,Follow
from .serializers import DealSerializer, FollowSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
User = get_user_model()
from django.contrib.auth import login, logout,authenticate
from .serializers import LoginSerializer

class DealListAPIView(generics.ListCreateAPIView):
    queryset = Deal.objects.filter(is_approved=True).order_by('-created_at')
    serializer_class = DealSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DealDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)




class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):  
        following = get_object_or_404(User, id=user_id)  
        if following == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)
        if not created:
            return Response({"detail": "Already following."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)
        

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        try:
            follow = Follow.objects.get(follower=request.user, following_id=user_id)
            follow.delete()
            return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({"detail": "Not following."}, status=status.HTTP_400_BAD_REQUEST)


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)
    

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
