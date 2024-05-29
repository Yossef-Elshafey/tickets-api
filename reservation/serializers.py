from rest_framework import serializers

from reservation.models import Reservation


class ReservationSer(serializers.ModelSerializer):
    seat_names = serializers.CharField()

    class Meta:
        model = Reservation
        fields = "__all__"
