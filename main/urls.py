from django.urls import path
from .views import index, login_view, track_detail, logout_view, add_to_collection, collection_view, search_api

urlpatterns = [
    path('', login_view, name='login'),
    path('index/', index, name='index'),
    path('track/<int:track_id>/', track_detail, name='track_detail'),


    path('logout/', logout_view, name='logout'),
    path('add-to-collection/<int:track_id>/', add_to_collection, name='add_to_collection'),
    path('collection/', collection_view, name='collection'),
    path('api/search/', search_api, name='search_api'),
]
