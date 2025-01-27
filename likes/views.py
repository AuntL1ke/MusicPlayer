from django.shortcuts import render, redirect
import requests

def toggle_like(request, track_id):
    """Функція для додавання або видалення треку з лайкнутого плейлісту."""
    playlist = request.session.get('playlist', [])
    
    if track_id in playlist:
        playlist.remove(track_id)  # Видалити трек, якщо він уже в плейлісті
    else:
        playlist.append(track_id)  # Додати трек, якщо його ще немає
    
    request.session['playlist'] = playlist  # Оновити сесію
    request.session.modified = True  # Позначити сесію як змінену
    
    # Повернутися на попередню сторінку
    return redirect(request.META.get('HTTP_REFERER', '/'))

def fetch_track_by_id(track_id):
    """
    Функція для отримання інформації про трек через API на основі track_id.
    """
    url = f"https://api.deezer.com/track/{track_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'id': data['id'],
            'title': data['title'],
            'artist': data['artist']['name'],
            'cover': data['album']['cover_medium'],
            'preview': data['preview'],
        }
    return None

def playlist(request):
    """Функція для відображення сторінки плейлісту."""
    playlist = request.session.get('playlist', [])  # Отримати список треків із сесії
    liked_tracks = []
    
    # Отримуємо інформацію про кожен лайкнутий трек через API
    for track_id in playlist:
        track = fetch_track_by_id(track_id)
        if track:
            liked_tracks.append(track)
    
    return render(request, 'playlist.html', {'liked_tracks': liked_tracks})
