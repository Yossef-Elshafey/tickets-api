from django.urls import path
from . import views

urlpatterns = [
    path("reservation", views.ListReservation.as_view()),
    path("reservation/<int:id>", views.SingleReservation.as_view()),
]
