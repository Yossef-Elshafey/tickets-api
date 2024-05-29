from django.urls import path
from . import views

urlpatterns = [
    path("reservation", views.ListReservation.as_view()),
]
