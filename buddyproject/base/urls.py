"""buddyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"), 
    path('create-room/', views.createRoom, name="create-room"), 
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>', views.userProfilePage, name="profile"),
    path('update-profile/', views.updateProfile, name="update-profile"),
    path('topics/', views.topicsPage, name="topics"),
]
