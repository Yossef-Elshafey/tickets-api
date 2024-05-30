from rest_framework import serializers

from hall.models import Hall
from movies.models import Movie
from reservation.models import Reservation


class CustomValidation:
    def check_cap(self, movie, seat_required):
        """
        getting hall instance from the instance came from payload
        check if the current hall able to carry this reservation
        since the app is demo / practical,
        there isn't like party table determine the hall availablity,
        increment / dec relying on the reservations the hall is getting
        the validation would be if some one tries to reserve the whole hall
        """
        if movie:
            hall = Hall.objects.get(id=movie.hall_id.id)
        else:
            raise serializers.ValidationError("movie doesn't exist")

        free_seat = hall.max_seat - seat_required

        if 0 > free_seat:
            raise serializers.ValidationError(
                f"couldn't reserve {seat_required} required seats available:{hall.max_seat}"
            )

        return True

    @staticmethod
    def raise_(msg):
        raise msg

    def validate_seat_names(self, num_of_seats, names):
        """
        check if num_of_seats is the same as the seat names in payload
        """
        if num_of_seats and names:
            names_count = len(names.split(","))
            print(names_count == num_of_seats)

            # this look trash but i love python hacks
            return (
                True
                if num_of_seats == names_count
                else self.raise_(
                    serializers.ValidationError(
                        "seat names doesn't match the num of seats reserverd"
                    )
                )
            )


class ReservationSer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        vald = CustomValidation()
        nos = validated_data["num_of_seats"]
        # if something went wrong raise experssion will be raised
        vald.check_cap(validated_data["movie_id"], nos)
        vald.validate_seat_names(nos, validated_data["seat_names"])
        reservation = Reservation.objects.create(**validated_data)
        return reservation
