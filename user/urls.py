from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import (
    UserSignupAPIView,
    UserMeAPIView,
    UserPublicAPIView,
    UserChangePasswordAPIView,
)

app_name = "user"
router = DefaultRouter()

urlpatterns = [
    path("", UserSignupAPIView.as_view()),
    path("me", UserMeAPIView.as_view()),
    path("change-password", UserChangePasswordAPIView.as_view()),
    path("@<str:account>", UserPublicAPIView.as_view()),
]


urlpatterns += router.urls
