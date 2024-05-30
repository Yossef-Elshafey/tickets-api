from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serailizers import SigninSer, SignupSer


class SigninView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SigninSer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            user = self.queryset.get(email=serializer.validated_data.get("email"))
            if not user.check_password(serializer.validated_data.get("password")):
                return Response(
                    {"error": "invalid creds"}, status=status.HTTP_400_BAD_REQUEST
                )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid creds"}, status=status.HTTP_400_BAD_REQUEST
            )


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "id": user.id}, status=status.HTTP_201_CREATED
        )


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        Token.objects.get(user=user).delete()
        return Response("", status=status.HTTP_204_NO_CONTENT)
