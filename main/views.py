import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import random

def search_tracks(query):
    """
    Функція для пошуку треків. Якщо запит порожній, повертаємо популярні треки.
    """
    url = f"https://api.deezer.com/chart" if not query else f"https://api.deezer.com/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        items = data['tracks']['data'] if not query and 'tracks' in data else data.get('data', [])
        for item in items:
            tracks.append({
                'id': item['id'],
                'title': item['title'],
                'artist': item['artist']['name'],
                'cover': item['album']['cover_medium'],
                'preview': item['preview'],
            })
        return tracks
    return []

def fetch_all_tracks(query):
    """
    Функція для отримання треків з API Deezer (обмежена кількістю для пагінації).
    """
    base_url = f"https://api.deezer.com/search?q={query}"
    response = requests.get(base_url)
    tracks = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get('data', []):
            tracks.append({
                'id': item['id'],
                'title': item['title'],
                'artist': item['artist']['name'],
                'cover': item['album']['cover_medium'],
                'preview': item['preview'],
            })
    return tracks

def search_api(request):
    """
    Django API-представлення для пошуку треків.
    """
    query = request.GET.get('query', '')
    tracks = fetch_all_tracks(query) if query else search_tracks('')
    return JsonResponse({'results': tracks})

def index(request):
    query = request.GET.get('query', '')  # Отримуємо запит користувача
    tracks = search_tracks(query)  # Завантажуємо всі треки для обраного запиту
    paginator = Paginator(tracks, 10)  # Розбиваємо на сторінки (10 треків на сторінку)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'user_type': 'Guest',
        'query': query,
    })

def track_detail(request, track_id):
    query = request.GET.get('query', '')
    tracks = search_tracks(query) if query else search_tracks('')  # Завантажуємо всі треки
    track = next((t for t in tracks if str(t['id']) == str(track_id)), None)  # Порівнюємо як рядки

    if track:
        return render(request, 'track_detail.html', {'track': track})

    return redirect('index')
