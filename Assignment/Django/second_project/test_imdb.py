import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

r = requests.get('https://www.imdb.com/title/tt0468569/fullcredits', headers=headers)
cast = re.findall(r'<td class="primary_photo">.*?<img alt="([^"]+)"', r.text, re.DOTALL)
print(cast[:15])
