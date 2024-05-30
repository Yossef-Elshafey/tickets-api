from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    class Meta:
        db_table = "Reservation"

    movie_id = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="movies",
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    num_of_seats = models.IntegerField()

    def __str__(self):
        return f"{ self.customer } { self.movie_id }"


class Seat(models.Model):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="seats"
    )
    seat_name = models.CharField(max_length=255)  # a2, a3, b3, b4, etc.

    class Meta:
        db_table = "reserved_seats"
