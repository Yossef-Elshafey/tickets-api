from rest_framework import generics, permissions
from rest_framework.views import Response

from reservation.models import Reservation
from reservation.serializers import ReservationSer


class ListReservation(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.prefetch_related("movie_id", "customer").all()
    serializer_class = ReservationSer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset().filter(customer=user)
        serailizer = self.get_serializer(queryset, many=True)
        return Response(serailizer.data)
