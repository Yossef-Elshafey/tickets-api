from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Movie
from hall.serializers import HallSer
from hall.models import Hall


class MoviesSer(serializers.ModelSerializer):
    hall = HallSer(required=False, source="hall_id")
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), write_only=True
    )

    class Meta:
        model = Movie
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Movie.objects.select_related("hall_id").all(),
                fields=("name", "release_date"),
                message="name / release_date already exist",
            )
        ]

    def create(self, data):
        print(data)
        return Movie.objects.create(**data)
