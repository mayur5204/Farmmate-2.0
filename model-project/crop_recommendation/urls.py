from django.urls import path
from . import views

urlpatterns = [
    path('', views.croprecommendation, name='croprecommendation'),
    path('result/', views.result, name='result'),
]