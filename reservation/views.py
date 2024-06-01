from django.db.models.query import Q
from rest_framework import generics, permissions
from rest_framework.views import Response
from reservation.models import Reservation
from reservation.serializers import ReservationSer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.customer == request.user:
            return True
        return False


class ListReservation(generics.ListCreateAPIView):
    # ay 7ad y2dr y3ml post bas lma y3ml get hygelo 7agto bas
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

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset().filter(
            Q(customer=self.request.user.id) & Q(id=self.kwargs["id"])
        )
        serailizer = self.get_serializer(queryset, many=True)
        return Response(serailizer.data)
