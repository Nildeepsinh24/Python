import os
import django
import urllib.request, urllib.error

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()
from cine_verse.models import Movie

updates = {
    'Breaking Bad': 'https://m.media-amazon.com/images/I/91+GrGr5TWL._AC_UF894,1000_QL80_.jpg',
    'Succession': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQu-dnn_g6RXHIHXtnSpgMkQaAepqifnlxa-w&s',
    'The Office': 'https://wallpapercat.com/w/full/2/1/c/172040-2880x1800-desktop-hd-the-office-tv-series-wallpaper.jpg',
    'Friends': 'https://wallpapercat.com/w/full/0/3/b/13917-1154x2048-mobile-hd-friends-tv-series-background-photo.jpg',
    'Ted Lasso': 'https://images3.alphacoders.com/140/thumb-1920-1407723.webp',
    'Wednesday': 'https://images.wallpapersden.com/image/download/netflix-wednesday-2022_bW1mbm2UmZqaraWkpJRmbmdlrWZlbWU.jpg',
}

for title, url in updates.items():
    qs = Movie.objects.filter(title=title)
    if not qs.exists():
        print(f'{title} -> NOT FOUND')
        continue
    qs.update(poster_url=url)
    verify = 'N/A'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            code = r.getcode()
            ctype = r.headers.get('Content-Type', '')
            if code == 200 and ctype.startswith('image'):
                verify = 'OK'
            else:
                verify = f'BAD_RESPONSE({code},{ctype})'
    except urllib.error.HTTPError as e:
        verify = f'HTTPError({e.code})'
    except Exception as e:
        verify = f'ERROR({e.__class__.__name__})'
    print(f"{title} | UPDATED | {verify} -> {url}")
