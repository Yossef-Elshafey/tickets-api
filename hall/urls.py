from django.urls import path
from . import views

urlpatterns = [
    path("hall", views.HallView.as_view()),
    path("hall/<int:id>", views.SingleHall.as_view()),
]
