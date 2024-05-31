from rest_framework import generics, permissions
from movies.models import Movie
from movies.serailizers import MoviesSer
from rest_framework.pagination import PageNumberPagination


class CustomMoviePaginator(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 10
    page_query_param = "p"


class CreateMovie(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MoviesSer
    pagination_class = CustomMoviePaginator


class ListMovies(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MoviesSer
    pagination_class = CustomMoviePaginator


class SingleMovie(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MoviesSer
    lookup_field = "id"
