"""dentaclinic URL Configuration

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
from django.urls import path
from . import views
from .views import create_appointment, appointment_detail, manager_actions, available_slots
urlpatterns = [
    # path('profile', views.profile, name='profile'),
    path('', views.index, name='index'),
    path('create/', create_appointment, name='create_appointment'),
    path('available_slots/', available_slots, name='available_slots'),
    path('<int:pk>/', appointment_detail, name='appointment_detail'),
    path('<int:pk>/actions/', manager_actions, name='manager_actions'),
]
