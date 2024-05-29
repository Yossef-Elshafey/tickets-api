from django.db import models
from django.db.models.aggregates import Sum

from reservation.models import Reservation


class Hall(models.Model):
    class Meta:
        db_table = "Hall"

    name = models.CharField(max_length=10)
    max_seat = models.IntegerField()

    def capacity_check(self):
        # Aggregate the number of seats reserved for this specific hall
        reservation = Reservation.objects.filter(hall_id=self.id).aggregate(
            seats_reserved=Sum("num_of_seats")
        )
        seats_reserved = reservation["seats_reserved"] or 0
        return True if self.max_seat > seats_reserved else False

    def __str__(self):
        return self.name
