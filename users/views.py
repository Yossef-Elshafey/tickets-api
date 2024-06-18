from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.serailizers import AdminUserSer, SigninSer, SignupSer


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
            return Response(
                {"token": token.key, "id": user.id, "admin": user.is_superuser},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid creds"}, status=status.HTTP_400_BAD_REQUEST
            )


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {"token": token.key, "id": user.id}, status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response({"username": ["first/last name already exist"]})


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        Token.objects.get(user=user).delete()
        return Response("", status=status.HTTP_204_NO_CONTENT)


class MyUser(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        query = User.objects.get(id=user.id)
        ser = SignupSer(query)
        return Response(ser.data)


class AdminUser(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AdminUserSer

    def create(self, request, *args, **kwargs):
        try:
            print(self.request.data)
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {"token": token.key, "id": user.id, "isAdmin": True},
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError:
            return Response(
                "User exists",
                status=status.HTTP_400_BAD_REQUEST,
            )
