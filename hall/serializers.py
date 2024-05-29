from rest_framework import serializers

from hall.models import Hall


class HallSer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Hall
