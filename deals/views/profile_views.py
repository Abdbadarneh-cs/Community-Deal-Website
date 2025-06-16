from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..serializers.user_serializer import UserSerializer

class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user