from django.contrib import admin

from reservation.models import Reservation, Seat

admin.site.register(Reservation)
admin.site.register(Seat)
