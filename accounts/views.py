from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from .serializers import ForgotPasswordSerializer, RegisterSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Forgot Password (generate token) 
class ForgotPasswordView(APIView):
    authentication_classes = []   
    permission_classes = []       

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        payload = {
            "user_id": str(user.id),
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        reset_link = f"http://localhost:3000/reset-password/{token}/"

        print("Reset link:", reset_link)

        return Response({
            "message": "Reset link generated successfully",
            "token": token
        }, status=status.HTTP_200_OK)


# Reset Password
class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request,):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["password"]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=400)
        except jwt.DecodeError:
            return Response({"error": "Invalid token"}, status=400)
        
        user.set_password(new_password)
        user.save()
        

        return Response({
            "message": "Password updated successfully"
        }, status=status.HTTP_200_OK)
    
# subscription     
class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered"})

        return Response(serializer.errors)

