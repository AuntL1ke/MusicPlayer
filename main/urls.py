from django.urls import path
from . import views  # Імпортуємо views з додатку main
from likes import views as likes_views  # Імпортуємо views з додатку likes

urlpatterns = [
    path('', views.index, name='index'),  # Головна сторінка
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),  # Деталі треку
    path('api/search/', views.search_api, name='search_api'),  # API пошуку
    path('playlist/', likes_views.playlist, name='playlist'),
    path('toggle-like/<int:track_id>/', likes_views.toggle_like, name='toggle_like'),# Сторінка плейлісту
]
