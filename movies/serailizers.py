from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Movie


class MoviesSer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Movie.objects.all(),
                fields=("name", "release_date"),
                message="name / release_date already exist",
            )
        ]
        depth = 1
        extra_kwargs = {"slug": {"read_only": True}}
