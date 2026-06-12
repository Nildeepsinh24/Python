import os
import sys
import django
import urllib.request
import urllib.error

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
try:
    django.setup()
except Exception as e:
    print('Django setup failed:', e)
    sys.exit(1)

from cine_verse.models import Movie

movies = Movie.objects.all()
print(f'Found {movies.count()} movies to check')

broken = []

for m in movies:
    url = (m.poster_url or '').strip()
    if not url:
        broken.append((m.id, m.title, 'empty url'))
        print(f'[{m.id}] {m.title} -> empty URL')
        continue
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            code = res.getcode()
            ctype = res.headers.get('Content-Type', '')
            if code != 200 or not ctype.startswith('image'):
                broken.append((m.id, m.title, f'status={code}, type={ctype}'))
                print(f'[{m.id}] {m.title} -> status={code}, type={ctype}')
            else:
                print(f'[{m.id}] {m.title} -> OK ({code}, {ctype})')
    except urllib.error.HTTPError as he:
        broken.append((m.id, m.title, f'HTTPError {he.code}'))
        print(f'[{m.id}] {m.title} -> HTTPError {he.code}')
    except urllib.error.URLError as ue:
        broken.append((m.id, m.title, f'URLError {ue.reason}'))
        print(f'[{m.id}] {m.title} -> URLError {ue.reason}')
    except Exception as e:
        broken.append((m.id, m.title, str(e)))
        print(f'[{m.id}] {m.title} -> Exception {e}')

print('\nSummary:')
print(f'Total checked: {movies.count()}')
print(f'Broken or suspicious: {len(broken)}')
for b in broken[:20]:
    print(f'- {b[0]} | {b[1]} | {b[2]}')

if broken:
    sys.exit(2)
else:
    sys.exit(0)
