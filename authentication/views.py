from rest_framework.views import APIView
from django.http import JsonResponse
from .serializer import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(
                {"errors": serializer.errors, "message": "Login failed"}, status=400
            )
        
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login successful"
        }, status=200)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data
        serializer = RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return JsonResponse(
                {"errors": serializer.errors, "message": "Registration failed"}, status=400
            )

        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )

        return JsonResponse(
            {"message": "Registration successful", "user_id": user.id}, status=201
        )