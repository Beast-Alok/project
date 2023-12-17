
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('login_index/', views.login_index, name="login_index"),
    path('user_logout/', views.user_logout, name="user_logout"),
]
