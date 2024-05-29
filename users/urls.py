from django.urls import path
from . import views

urlpatterns = [
    path("users/sign-in", views.SigninView.as_view()),
    path("users/sign-up", views.SignUpView.as_view()),
]
