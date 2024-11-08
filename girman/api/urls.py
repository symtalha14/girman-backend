from django.urls import path
from .views import searchUser, createFTS

urlpatterns = [
    path("users/search", searchUser),
    path("create-fts", createFTS)
]