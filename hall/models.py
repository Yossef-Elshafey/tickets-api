from django.db import models
from django.db.models.aggregates import Sum

from reservation.models import Reservation


class Hall(models.Model):
    class Meta:
        db_table = "Hall"

    name = models.CharField(max_length=10)
    max_seat = models.IntegerField()

    def __str__(self):
        return self.name
