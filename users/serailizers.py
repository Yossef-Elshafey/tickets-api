from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.validators import UniqueValidator


class CustomValidators:
    @staticmethod
    def non_blank(value):
        if value is None:
            raise serializers.ValidationError("field required")

    @staticmethod
    def password_validations(attrs):
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


class SigninSer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "password")
        model = User


class SignupSer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email exist")]
    )
    password_compare = serializers.CharField(write_only=True)
    first_name = CharField(validators=[CustomValidators.non_blank])
    last_name = CharField(validators=[CustomValidators.non_blank])

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password_compare",
            "id",
        )
        model = User
        extra_kwargs = {"id": {"read_only": True}}  # same ser used in MyUser

    # for the same usage in MyUser this serializers spending huge effort may he will have a good life
    def to_representation(self, instance):
        inst = model_to_dict(instance)
        inst.pop("password")
        return inst

    def validate(self, attrs):
        CustomValidators.password_validations(attrs=attrs)
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_compare")
        validated_data["password"] = make_password(validated_data.get("password"))
        username = f"{validated_data['first_name'] } { validated_data['last_name'] }"
        user = User.objects.create(username=username, **validated_data)
        return user


class AdminUserSer(serializers.ModelSerializer):
    password_compare = serializers.CharField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email exist")]
    )
    first_name = serializers.CharField(validators=[CustomValidators.non_blank])
    last_name = CharField(validators=[CustomValidators.non_blank])

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password_compare",
        )
        model = User
        extra_kwargs = {
            "password_compare": {"write_only": True},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        CustomValidators.password_validations(attrs=attrs)
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_compare")
        validated_data["password"] = make_password(validated_data["password"])
        username = f"{validated_data['first_name'] } { validated_data['last_name'] }"
        user = User.objects.create(
            username=username, is_staff=True, is_superuser=True, **validated_data
        )
        return user
