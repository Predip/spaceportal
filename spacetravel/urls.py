from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('info/', views.space_info, name='space_info'),
    path('asteroids/', views.asteroids_explorer, name='asteroids_explorer'),
    path('weather/', views.weather_info, name='weather'),
    path('news/', views.news_collection, name='news'),
]
