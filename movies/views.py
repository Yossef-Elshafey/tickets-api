from rest_framework import generics, permissions
from movies.models import Movie
from movies.serailizers import MoviesSer
from rest_framework.pagination import PageNumberPagination


class CustomMoviePaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 10
    page_query_param = "p"


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method not in permissions.SAFE_METHODS and request.user.is_superuser:
            return True
        return False


class CreateMovie(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Movie.objects.select_related("hall_id").all()
    serializer_class = MoviesSer
    # pagination_class = CustomMoviePaginator


class ListMovies(generics.ListAPIView):
    queryset = Movie.objects.select_related("hall_id").all()
    serializer_class = MoviesSer
    pagination_class = CustomMoviePaginator
    permission_classes = [permissions.AllowAny]


class SingleMovie(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.select_related("hall_id").all()
    serializer_class = MoviesSer
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly]
