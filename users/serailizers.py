from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.fields import EmailField
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.validators import UniqueValidator


class SigninSer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "password")
        model = User


class SignupSer(serializers.ModelSerializer):
    @staticmethod
    def required(value):
        if value is None:
            raise serializers.ValidationError("field required")

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_compare = serializers.CharField(write_only=True)
    first_name = CharField(validators=[required])
    last_name = CharField(validators=[required])

    class Meta:
        fields = ("first_name", "last_name", "email", "password", "password_compare")
        model = User

    def validate(self, attrs):
        password = attrs["password"]
        pass_match = attrs["password_compare"]
        if not password == pass_match:
            raise serializers.ValidationError({"password": ["password didn't match"]})

        pass_len = 6
        if pass_len >= len(password):
            raise serializers.ValidationError(
                {
                    "password": [
                        "password cannot be less than or equal {} ".format(pass_len)
                    ]
                }
            )

        return attrs

    def create(self, validated_data):
        non_compare = validated_data.pop("password_compare")
        validated_data["password"] = make_password(validated_data.get("password"))
        username = f"{validated_data['first_name'] } { validated_data['last_name'] }"
        user = User.objects.create(username=username, **validated_data)
        return user
