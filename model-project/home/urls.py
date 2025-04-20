from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('resources/', views.resources, name='resources'),
    path('help/', views.help, name='help'),
]
