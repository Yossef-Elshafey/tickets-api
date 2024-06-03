from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.views import Response, status
from hall.models import Hall
from hall.serializers import HallSer
from movies.models import Movie


class HallView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Hall.objects.all()
    serializer_class = HallSer


class SingleHall(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Hall.objects.all()
    serializer_class = HallSer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        try:
            self.queryset.filter(id=self.kwargs["id"]).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            assigned_movie = Movie.objects.select_related("hall_id").filter(
                hall_id=self.kwargs["id"]
            )
            response = []
            for movie in assigned_movie:
                response.append(movie.name)
            return Response(
                f"hall have {'-'.join(response)} movies assigned delete movies first"
            )
