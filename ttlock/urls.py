from django.urls import path

from . import views
from .views import update_or_auto_create_user, list_users, add_phone_user, create_new_user, update_or_auto_create_user2
urlpatterns = [
    path("api/test/", update_or_auto_create_user),
    path("api/test2/", update_or_auto_create_user2),
    path("", list_users),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("accounts/profile/", views.redirect_home),
    path("api/create_points", views.create_points),
    path("api/open_door", views.open_door),
    path("api/write_list_notify_group", views.write_list_notify_group),
    path("api/write_list_notify_students", views.write_list_notify_students)

]
