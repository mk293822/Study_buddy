from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_viw, name='home'),
    path('roomDetails/<str:pk>/', views.room_details, name='roomDetails'),
    path('roomCreate/', views.room_create, name='roomCreate'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('deleteRoom/<str:pk>/', views.delete_room, name='delete-room'),
    path('deleteMessage/<str:pk>/', views.delete_message, name='delete-message'),
    path('userInfo/<str:pk>/', views.userInfo_view, name='user-info'),
    path('edituser/', views.edit_user_view, name='edit-user'),
]