from django.db import migrations

def seed_data(apps, schema_editor):
    Genre = apps.get_model('cine_verse', 'Genre')
    Movie = apps.get_model('cine_verse', 'Movie')
    
    # Genres to ensure
    genres_to_ensure = [
        ("Action", "action"),
        ("Drama", "drama"),
        ("Thriller", "thriller"),
        ("Comedy", "comedy"),
        ("Crime", "crime"),
        ("Mystery", "mystery")
    ]
    
    genre_objects = {}
    for name, slug in genres_to_ensure:
        genre, created = Genre.objects.get_or_create(slug=slug, defaults={"name": name})
        genre_objects[slug] = genre
        
    # Define series data
    series_data = [
        {
            "title": "The Family Man",
            "description": "Srikant Tiwari is a middle-class man who seems to lead an ordinary, mundane life. In reality, he is a senior analyst for TASC, a secret espionage wing of the National Investigation Agency. While working under extreme pressure to protect the nation from terrorist threats and high-stakes conspiracies, Srikant must also navigate the everyday challenges of family life, keeping his secret career hidden from his suspicious wife and children.",
            "content_type": "series",
            "poster_url": "https://image.tmdb.org/t/p/original/bGukv7oQqTuD5PY1FaSv5YSqYln.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/eEzKigDI64OomZV6VTJvoPGmVu1.jpg",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "rating": 8.7,
            "release_year": 2019,
            "language": "Hindi",
            "duration": "2 Seasons (19 Episodes)",
            "is_trending": True,
            "is_popular": True,
            "is_latest": False,
            "is_top_rated": True,
            "cast": "Manoj Bajpayee, Priyamani, Sharib Hashmi, Samantha Ruth Prabhu, Ashlesha Thakur, Vedant Sinha, Shreya Dhanwanthary, Sharad Kelkar, Sunny Hinduja, Neeraj Madhav",
            "crew": "Director: Raj Nidimoru, Krishna D.K., Suparn S. Verma",
            "genres": ["action", "drama", "thriller", "comedy"]
        },
        {
            "title": "Asur: Welcome to Your Dark Side",
            "description": "Set against the mystical backdrop of Varanasi, this psychological thriller follows Nikhil Nair, a former forensic expert turned teacher, who is called back to the CBI to assist his mentor Dhananjay Rajpoot. Together, they confront a mysterious, brilliant serial killer who uses mythological concepts from Hindu philosophy to justify his brutal murders, claiming to be the incarnation of the demon Kali.",
            "content_type": "series",
            "poster_url": "https://image.tmdb.org/t/p/original/9AZnfGUnPZBBJJDtYk5Uoxw4IMf.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/eXUr34XTqYaDwyOerFpL6sUOgDL.jpg",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "rating": 8.5,
            "release_year": 2020,
            "language": "Hindi",
            "duration": "2 Seasons (16 Episodes)",
            "is_trending": True,
            "is_popular": True,
            "is_latest": False,
            "is_top_rated": True,
            "cast": "Arshad Warsi, Barun Sobti, Anupriya Goenka, Riddhi Dogra, Amey Wagh, Sharib Hashmi, Abhishek Chauhan, Meiyang Chang",
            "crew": "Director: Oni Sen",
            "genres": ["drama", "thriller", "mystery", "crime"]
        }
    ]
    
    for item in series_data:
        movie, created = Movie.objects.update_or_create(
            title=item["title"],
            defaults={
                "description": item["description"],
                "content_type": item["content_type"],
                "poster_url": item["poster_url"],
                "banner_url": item["banner_url"],
                "video_url": item["video_url"],
                "rating": item["rating"],
                "release_year": item["release_year"],
                "language": item["language"],
                "duration": item["duration"],
                "is_trending": item["is_trending"],
                "is_popular": item["is_popular"],
                "is_latest": item["is_latest"],
                "is_top_rated": item["is_top_rated"],
                "cast": item["cast"],
                "crew": item["crew"]
            }
        )
        
        movie.genres.clear()
        for g_slug in item["genres"]:
            movie.genres.add(genre_objects[g_slug])

def rollback_seed(apps, schema_editor):
    Movie = apps.get_model('cine_verse', 'Movie')
    Movie.objects.filter(title__in=["The Family Man", "Asur: Welcome to Your Dark Side"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('cine_verse', '0005_userprofile_favorites_order_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, rollback_seed),
    ]
