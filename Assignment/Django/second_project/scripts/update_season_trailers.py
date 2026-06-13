import os
import sys
import django
import time
from youtubesearchpython import VideosSearch

# Setup path and django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()

from cine_verse.models import Movie

def fetch_trailer_url(query):
    try:
        videosSearch = VideosSearch(query, limit = 1)
        results = videosSearch.result()['result']
        if results:
            return results[0]['link']
    except Exception as e:
        print(f"Error searching YouTube for {query}: {e}")
    return None

def update_trailers():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Connected to database:", django.db.connection.settings_dict['NAME'])
    
    # We only want to update SEASONS of SERIES.
    # Exclude "Stranger Things" as requested by the user.
    seasons = Movie.objects.filter(
        content_type='series', 
        part_name__icontains='Season'
    ).exclude(title__icontains='Stranger Things')
    
    updated_count = 0
    print(f"Found {seasons.count()} seasons to update.")
    
    for season in seasons:
        # e.g., "Breaking Bad" and "Season 1"
        parent_title = season.parent.title if season.parent else season.title.split(':')[0]
        part_name = season.part_name
        
        # Query format: "Breaking Bad Season 1 official trailer"
        query = f"{parent_title} {part_name} official trailer"
        print(f"Searching for: {query}")
        
        youtube_url = fetch_trailer_url(query)
        
        if youtube_url:
            season.video_url = youtube_url
            season.save(update_fields=['video_url'])
            print(f"  -> Assigned: {youtube_url}")
            updated_count += 1
        else:
            print(f"  -> Failed to find trailer.")
            
        time.sleep(0.5) # Be polite to YouTube APIs
            
    print(f"\nDone! Updated trailers for {updated_count} seasons.")

if __name__ == "__main__":
    update_trailers()
