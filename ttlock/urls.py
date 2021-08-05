
from django.urls import path
from .views import update_or_auto_create_user, list_users, add_phone_user, create_new_user
urlpatterns = [
    path("api/test/", update_or_auto_create_user),
    path("", list_users),
]
