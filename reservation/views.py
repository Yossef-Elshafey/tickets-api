from django.db.models.query import Q
from rest_framework import generics, permissions
from rest_framework.views import Response
from reservation.models import Reservation
from reservation.serializers import ReservationSer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user


class ListReservation(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.prefetch_related("movie_id", "customer").all()
    serializer_class = ReservationSer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset().filter(customer=user)
        serailizer = self.get_serializer(queryset, many=True)
        return Response(serailizer.data)


class SingleReservation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Reservation.objects.prefetch_related("movie_id", "customer").all()
    serializer_class = ReservationSer
    lookup_field = "id"

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(), id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj
