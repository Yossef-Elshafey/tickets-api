from django.shortcuts import render
from rest_framework import generics

from reservation.models import Reservation
from reservation.serializers import ReservationSer


class ListReservation(generics.ListCreateAPIView):
    queryset = Reservation.objects.prefetch_related("movie_id", "customer").all()
    serializer_class = ReservationSer
