# from rest_framework.generics import GenericAPIView 
# from rest_framework.response import Response
# from django.contrib.auth import authenticate, login, logout, get_user_model
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from ..serializers import LoginSerializer,RegisterSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status,generics,permissions
# from ..serializers import user_serializer


# User = get_user_model()

# class LoginView(GenericAPIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
#             if device:
#                 request.session['pre_otp_user_id'] = user.id
#                 logout(request)
#                 return Response({'otp_required': True}, status=200)
#             login(request, user)
#             return Response({'message': 'Login successful'}, status=200)
#         return Response({'error': 'Invalid credentials'}, status=400)

# class UserLoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class RegisterAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]

# class UserLogoutAPIView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)