from accounts.models import RequestCount
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import User
from . import serializers as serial


class RequestCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request_count = RequestCount.objects.first()
        return Response(
            {'requests': request_count.count if request_count else 0},
            status=status.HTTP_200_OK)


class RequestCountResetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        RequestCount.objects.update_or_create(id=1, defaults={'count': 0})
        return Response({'message': 'Request count reset successfully.'},
                        status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serial.UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                response = get_tokens_for_user(user)
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "User with this username already exists!"},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serial.UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,
                                username=username,
                                password=password)
            if user:
                response = get_tokens_for_user(user)
                return Response(response, status=status.HTTP_200_OK)

            user = User.objects.filter(username=username).first()
            if not user:
                return Response(
                    {"error": "Please provide correct username!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'error': 'Gimport requests Password is not correct!'},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
