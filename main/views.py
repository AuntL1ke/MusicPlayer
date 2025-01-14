import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import random

def search_tracks(query):
    # Якщо запит порожній, шукаємо популярні треки
    if not query:
        url = "https://api.deezer.com/chart"  # Повертає популярні треки
    else:
        url = f"https://api.deezer.com/search?q={query}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        
        # Якщо порожній запит, працюємо з "tracks" із chart
        if not query and 'tracks' in data:
            items = data['tracks']['data']
        else:
            items = data.get('data', [])
        
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

import requests
from django.http import JsonResponse

def fetch_all_tracks(query):
    """
    Функція для отримання всіх треків з API Deezer за допомогою пагінації.
    """
    base_url = f"https://api.deezer.com/search?q={query}"
    tracks = []
    index = 0  # Початкова позиція для пагінації
    limit = 25  # Кількість треків на одну сторінку (значення Deezer API за замовчуванням)

    while True:
        response = requests.get(f"{base_url}&index={index}")
        if response.status_code != 200:
            break  # Якщо запит не вдався, зупиняємо
        data = response.json()
        if 'data' not in data or not data['data']:
            break  # Якщо більше немає даних, зупиняємо
        # Додаємо треки до списку
        for item in data['data']:
            tracks.append({
                'id': item['id'],
                'title': item['title'],
                'artist': item['artist']['name'],
                'cover': item['album']['cover_medium'],
                'preview': item['preview'],
            })
        index += limit  # Переходимо до наступної сторінки

    return tracks


def search_api(request):
    """
    Django API-представлення для пошуку треків.
    """
    query = request.GET.get('query', '')
    if not query:  # Якщо запит порожній, повертаємо популярні треки
        tracks = search_tracks('')
    else:
        tracks = fetch_all_tracks(query)
    return JsonResponse({'results': tracks})


def index(request):
    # if not request.session.get('is_guest'):
    #     return redirect('login')
    
    query = request.GET.get('query', '')  # Отримуємо запит користувача
    tracks = search_tracks(query)
    paginator = Paginator(tracks, 10)  # Розбиваємо на сторінки (10 треків)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Передаємо результати пошуку в шаблон
    return render(request, 'index.html', {'page_obj': page_obj, 'user_type': 'Guest', 'query': query})

def track_detail(request, track_id):
    query = request.GET.get('query', '')
    tracks = fetch_all_tracks(query) if query else search_tracks('')  # Завантажуємо всі треки
    track = next((t for t in tracks if str(t['id']) == str(track_id)), None)  # Порівнюємо як рядки
    
    if track:
        return render(request, 'track_detail.html', {'track': track})
    
    # Якщо трек не знайдено, перенаправляємо на головну
    return redirect('index')

