from django.urls import path
from .views import searchUser, saveRecordsToMongo

urlpatterns = [
    path("users/search", searchUser),
    path("save-records", saveRecordsToMongo)
]