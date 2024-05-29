from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("movies", views.ListMovies.as_view()),
    path("movies/<int:id>", views.SingleMovie.as_view()),
]
