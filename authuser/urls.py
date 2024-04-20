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
urlpatterns = [
    # path('profile', views.profile, name='profile'),
    path('profile', views.profile, name='profile'),
    path('add_event/', views.add_event, name='add_event'),
    path('replace_status/', views.replace_status, name='replace_status'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
