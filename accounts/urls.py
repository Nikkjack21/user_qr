from django.urls import path
from accounts.views import (
    LoginView,
    RegisterView,
    CreateURLView,
    ListURLView,
    DeleteURLView,
    UpdateURLView,
    RedirectURLView,
    LogoutView,
)
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("create-url", CreateURLView.as_view(), name="create-url"),
    path("list-url", ListURLView.as_view(), name="list-url"),
    path("delete-url/<int:pk>", DeleteURLView.as_view(), name="delete-url"),
    path("update-url/<int:pk>", UpdateURLView.as_view(), name="update-url"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("<str:short_url>", RedirectURLView.as_view()),
]
