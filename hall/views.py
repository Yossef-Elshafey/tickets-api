from rest_framework import generics
from rest_framework.views import Response

from hall.models import Hall
from hall.serializers import HallSer


class HallView(generics.ListCreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSer


class UpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    pass


class SingleHall(UpdateDestroy):
    queryset = Hall.objects.all()
    serializer_class = HallSer
    lookup_field = "id"
