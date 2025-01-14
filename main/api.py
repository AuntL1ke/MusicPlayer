import requests
import urllib3
from django.http import JsonResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_tracks(query):
    url = f"https://api.deezer.com/search?q={query}"
    response = requests.get(url, verify=False)  # Вимикаємо перевірку SSL
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
