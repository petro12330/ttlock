
from django.urls import path

from . import views
from .views import update_or_auto_create_user, list_users, add_phone_user, create_new_user
urlpatterns = [
    path("api/test/", update_or_auto_create_user),
    path("", list_users),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
]
