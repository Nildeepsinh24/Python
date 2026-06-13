import os
import sys
import time
import requests
import re
import django
from urllib.parse import quote_plus

# Setup path and django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()

from cine_verse.models import Movie

def fetch_cast_from_tmdb(title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Clean up title for searching (e.g. "Breaking Bad: Season 1" -> "Breaking Bad")
    search_title = title.split(':')[0].strip()
    
    search_url = f'https://www.themoviedb.org/search?query={quote_plus(search_title)}'
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        # Find the first result URL
        match = re.search(r'href="(/((movie)|(tv))/\d+[^"]*)"', r.text)
        if match:
            url_path = match.group(1)
            # TMDB cast page
            cast_url = f"https://www.themoviedb.org{url_path}/cast"
            r2 = requests.get(cast_url, headers=headers, timeout=10)
            
            # Extract cast names using regex
            # TMDB cast lists names in a <p><a href="/person/...">Name</a></p> pattern
            cast_list = re.findall(r'<p><a href="/person/\d+-[^"]*">([^<]+)</a></p>', r2.text)
            
            # Deduplicate while preserving order
            seen = set()
            unique_cast = []
            for name in cast_list:
                if name not in seen:
                    unique_cast.append(name)
                    seen.add(name)
            
            # Return top 15 actors
            return unique_cast[:15]
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return []

def run():
    print("Connected to database:", django.db.connection.settings_dict['NAME'])
    movies = Movie.objects.exclude(title__endswith='Collection').exclude(title__endswith='Trilogy').exclude(title__endswith='Seasons')
    
    updated_count = 0
    for movie in movies:
        # If it's a parent collection holder or similar, skip
        if movie.part_number == 0 and 'Season' not in movie.title and not movie.parent:
            # wait, standalone movies also have part_number=0 and not parent.
            pass

        current_cast = movie.cast
        # Check if cast is empty or short
        if not current_cast or current_cast.count(',') < 8:
            print(f"Fetching extended cast for: {movie.title}")
            new_cast = fetch_cast_from_tmdb(movie.title)
            
            if new_cast and len(new_cast) > 3:
                cast_str = ", ".join(new_cast)
                movie.cast = cast_str
                movie.save(update_fields=['cast'])
                print(f"  -> Updated {movie.title} with {len(new_cast)} actors.")
                updated_count += 1
            else:
                print(f"  -> Failed to find extended cast for {movie.title}.")
            
            time.sleep(0.5) # Be polite to TMDB
        else:
            print(f"Skipping {movie.title}, already has {current_cast.count(',') + 1} actors.")
            
    print(f"\nDone! Updated {updated_count} records.")

if __name__ == '__main__':
    run()
