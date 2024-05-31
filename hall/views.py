from rest_framework import generics, permissions
from hall.models import Hall
from hall.serializers import HallSer


class HallView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hall.objects.all()
    serializer_class = HallSer


class SingleHall(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hall.objects.all()
    serializer_class = HallSer
    lookup_field = "id"
