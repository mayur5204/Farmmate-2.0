
from django.urls import path
from home import views



from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='homepage'),
    path('croprecommendation',views.croprecommendation, name='croprecommendation'),
    path('result/',views.result, name='result'),
    path('products/', views.products, name='products'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('resources/', views.resources, name='resources'),
    path('help/', views.help, name='help'),
    path('login/', views.login, name='login'),
    path('weather/', views.weather, name='weather'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
