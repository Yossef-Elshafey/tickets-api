from rest_framework import generics, permissions
from rest_framework.views import Response
from reservation.models import Reservation
from reservation.serializers import ReservationSer


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.user)
        return (
            True if obj.customer == request.user or request.user.is_superuser else False
        )


class ListReservation(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = (
        Reservation.objects.order_by("reservation_date")
        .select_related("movie_id", "customer", "movie_id__hall_id")
        .all()
    )
    serializer_class = ReservationSer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            queryset = self.get_queryset()
            serailizer = self.get_serializer(queryset, many=True)
            return Response(serailizer.data)
        queryset = self.get_queryset().filter(customer=user)
        serailizer = self.get_serializer(queryset, many=True)
        return Response(serailizer.data)


class SingleReservation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Reservation.objects.prefetch_related("movie_id", "customer").all()
    serializer_class = ReservationSer
    lookup_field = "id"

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(), id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj
