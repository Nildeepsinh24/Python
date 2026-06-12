import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','second_project.settings')
django.setup()
from cine_verse.models import Movie

titles = ['Interstellar','Inception','A Quiet Place','The Hangover','Friends']
for t in titles:
    try:
        m = Movie.objects.get(title=t)
        print(f"{t} -> {m.poster_url}")
    except Exception as e:
        print(f"{t} -> ERROR: {e}")
