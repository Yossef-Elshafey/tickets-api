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
    hall_id = models.ForeignKey(
        "hall.Hall", on_delete=models.CASCADE, related_name="hall"
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    num_of_seats = models.IntegerField()


class Seat(models.Model):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="seats"
    )
    seat_name = models.CharField(max_length=255)  # a2, a3, b3, b4, etc.
