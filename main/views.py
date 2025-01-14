import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

def search_tracks(query):
    url = f"https://api.deezer.com/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for item in data.get('data', []):
            tracks.append({
                'id': item['id'],
                'title': item['title'],
                'artist': item['artist']['name'],
                'cover': item['album']['cover_medium'],
                'preview': item['preview'],
            })
        return tracks
    return []

def search_api(request):
    query = request.GET.get('query', '')
    tracks = search_tracks(query)
    return JsonResponse({'results': tracks})


def login_view(request):
    if request.method == 'POST':
        if 'guest' in request.POST:
            request.session['is_guest'] = True
            return redirect('index')
    return render(request, 'login.html')

def index(request):
    if not request.session.get('is_guest'):
        return redirect('login')
    
    query = request.GET.get('query', '')  # Отримуємо запит користувача
    tracks = search_tracks(query)
    paginator = Paginator(tracks, 10)  # Розбиваємо на сторінки (10 треків)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Передаємо результати пошуку в шаблон
    return render(request, 'index.html', {'page_obj': page_obj, 'user_type': 'Guest', 'query': query})

    if not request.session.get('is_guest'):
        return redirect('login')
    
    query = request.GET.get('query', '')  # Пошук виконується за реальним запитом
    tracks = search_tracks(query)
    paginator = Paginator(tracks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'page_obj': page_obj, 'user_type': 'Guest', 'query': query})

def track_detail(request, track_id):
    # Отримуємо запит пошуку
    query = request.GET.get('query', '')
    tracks = search_tracks(query)  # Виконуємо пошук
    track = next((t for t in tracks if t['id'] == int(track_id)), None)  # Знаходимо трек за ID
    
    if track:
        return render(request, 'track_detail.html', {'track': track})
    
    # Якщо трек не знайдено, повертаємо на головну
    return redirect('index')


def logout_view(request):
    request.session.flush()
    return redirect('login')

def add_to_collection(request, track_id):
    track = next((t for t in search_tracks(request.GET.get('query', 'popular')) if t['id'] == int(track_id)), None)
    if track:
        if 'collection' not in request.session:
            request.session['collection'] = []
        request.session['collection'].append(track)
        request.session.modified = True
    return redirect('index')

def collection_view(request):
    collection = request.session.get('collection', [])
    return render(request, 'collection.html', {'collection': collection})
