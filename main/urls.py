from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Головна сторінка
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),  # Деталі треку
    path('api/search/', views.search_api, name='search_api'),  # API пошуку
]
