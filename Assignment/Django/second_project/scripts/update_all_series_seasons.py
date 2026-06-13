import os
import sys
import django

# Setup path and django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()

from cine_verse.models import Genre, Movie

print("Connected to database:", django.db.connection.settings_dict['NAME'])

# 1. Genres Map
genres_map = {}
for g_slug, g_name in [
    ('action', 'Action'),
    ('sci-fi', 'Sci-Fi'),
    ('drama', 'Drama'),
    ('thriller', 'Thriller'),
    ('comedy', 'Comedy'),
    ('horror', 'Horror'),
    ('adventure', 'Adventure'),
    ('crime', 'Crime'),
    ('mystery', 'Mystery'),
    ('biography', 'Biography'),
]:
    genre, _ = Genre.objects.get_or_create(slug=g_slug, defaults={'name': g_name})
    genres_map[g_slug] = genre

print("Genres loaded/created.")

# Helper to create/update movie
def upsert_movie(title, defaults, genre_slugs=[]):
    movie, created = Movie.objects.get_or_create(title=title, defaults=defaults)
    if not created:
        print(f"  Updating existing movie: {title}")
        for k, v in defaults.items():
            setattr(movie, k, v)
        movie.save()
    else:
        print(f"  Created new movie: {title}")
    
    # Add genres
    for g_slug in genre_slugs:
        if g_slug in genres_map:
            movie.genres.add(genres_map[g_slug])
            
    return movie

# ============================================================
# MOVIE FRANCHISES
# ============================================================

# -------------------------------------------------------
# 1. The Dark Knight Trilogy
# -------------------------------------------------------
print("\n--- The Dark Knight Trilogy ---")
try:
    dk_parent = Movie.objects.get(title="The Dark Knight")
    # Rename parent to trilogy collection
    dk_parent.title = "The Dark Knight Trilogy"
    dk_parent.duration = "3 Movies"
    dk_parent.description = "Christopher Nolan's groundbreaking trilogy following Bruce Wayne's journey from a grief-stricken young man to Gotham's legendary protector, Batman."
    dk_parent.release_year = 2012
    dk_parent.save()
    print(f"  Updated parent: The Dark Knight Trilogy")

    upsert_movie(
        title="Batman Begins",
        defaults={
            "description": "After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/8RW2runSEc34IwKN2D1eFcM3zzP.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/nMKdUUepR0i5zn0y1T4CsSB5ez.jpg",
            "video_url": "https://www.youtube.com/watch?v=neY2xVmOfUM",
            "rating": 8.8,
            "release_year": 2005,
            "language": "English",
            "duration": "2h 20m",
            "cast": "Christian Bale, Michael Caine, Liam Neeson, Katie Holmes, Gary Oldman",
            "crew": "Director: Christopher Nolan",
            "parent": dk_parent,
            "part_number": 1,
            "part_name": "Batman Begins"
        },
        genre_slugs=['action', 'drama', 'thriller']
    )

    upsert_movie(
        title="The Dark Knight",
        defaults={
            "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911javKOGQkXLTn.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/cfT29Im5VDvjE0RpyKOSdCKZal7.jpg",
            "video_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
            "rating": 9.7,
            "release_year": 2008,
            "language": "English",
            "duration": "2h 32m",
            "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Maggie Gyllenhaal, Gary Oldman",
            "crew": "Director: Christopher Nolan",
            "parent": dk_parent,
            "part_number": 2,
            "part_name": "The Dark Knight"
        },
        genre_slugs=['action', 'drama', 'thriller']
    )

    upsert_movie(
        title="The Dark Knight Rises",
        defaults={
            "description": "Eight years after the Joker's reign of anarchy, Batman, with the help of the enigmatic Catwoman, is forced from his exile to save Gotham City from the brutal guerrilla terrorist Bane.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/blXE8QLkCVDPPmE7yvAkKPTubJa.jpg",
            "video_url": "https://www.youtube.com/watch?v=g8evyE9TuYk",
            "rating": 9.0,
            "release_year": 2012,
            "language": "English",
            "duration": "2h 44m",
            "cast": "Christian Bale, Tom Hardy, Anne Hathaway, Joseph Gordon-Levitt, Gary Oldman",
            "crew": "Director: Christopher Nolan",
            "parent": dk_parent,
            "part_number": 3,
            "part_name": "The Dark Knight Rises"
        },
        genre_slugs=['action', 'drama', 'thriller']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'The Dark Knight' not found in DB")

# -------------------------------------------------------
# 2. John Wick Collection
# -------------------------------------------------------
print("\n--- John Wick Collection ---")
try:
    jw_parent = Movie.objects.get(title="John Wick: Chapter 4")
    jw_parent.title = "John Wick Collection"
    jw_parent.duration = "4 Movies"
    jw_parent.description = "The legendary saga of retired hitman John Wick, who is drawn back into the criminal underworld he tried to leave behind."
    jw_parent.release_year = 2023
    jw_parent.save()
    print(f"  Updated parent: John Wick Collection")

    upsert_movie(
        title="John Wick",
        defaults={
            "description": "An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/eBHjaEsQCYHRFiHbvUYqGnRaWSt.jpg",
            "video_url": "https://www.youtube.com/watch?v=C0BMx-qxsP4",
            "rating": 8.5,
            "release_year": 2014,
            "language": "English",
            "duration": "1h 41m",
            "cast": "Keanu Reeves, Michael Nyqvist, Alfie Allen, Willem Dafoe, Adrianne Palicki",
            "crew": "Director: Chad Stahelski",
            "parent": jw_parent,
            "part_number": 1,
            "part_name": "John Wick"
        },
        genre_slugs=['action', 'thriller']
    )

    upsert_movie(
        title="John Wick: Chapter 2",
        defaults={
            "description": "After returning to the criminal underworld to repay a debt, John Wick discovers that a large bounty has been put on his life.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/hXWBc7x4nx8eNZ8cMjRb2OI1MVt.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/mPGAMNpFrNH1rHFNfc5EXzJH9Ke.jpg",
            "video_url": "https://www.youtube.com/watch?v=ChpLV9AMqrk",
            "rating": 8.7,
            "release_year": 2017,
            "language": "English",
            "duration": "2h 2m",
            "cast": "Keanu Reeves, Common, Laurence Fishburne, Riccardo Scamarcio, Ian McShane",
            "crew": "Director: Chad Stahelski",
            "parent": jw_parent,
            "part_number": 2,
            "part_name": "Chapter 2"
        },
        genre_slugs=['action', 'thriller']
    )

    upsert_movie(
        title="John Wick: Chapter 3 - Parabellum",
        defaults={
            "description": "John Wick is on the run after killing a member of the international assassins' guild, and with a $14 million price tag on his head, he is the target of hit men and women everywhere.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/ziEuG1essDuWuC5lpWUaw1uXY2O.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/vVpEOvdxVBP2aV166j5Xlvb5yM6.jpg",
            "video_url": "https://www.youtube.com/watch?v=M7XM597XO94",
            "rating": 8.8,
            "release_year": 2019,
            "language": "English",
            "duration": "2h 11m",
            "cast": "Keanu Reeves, Halle Berry, Ian McShane, Laurence Fishburne, Asia Kate Dillon",
            "crew": "Director: Chad Stahelski",
            "parent": jw_parent,
            "part_number": 3,
            "part_name": "Chapter 3 - Parabellum"
        },
        genre_slugs=['action', 'thriller']
    )

    upsert_movie(
        title="John Wick: Chapter 4",
        defaults={
            "description": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/vZ02e421JxsoRWaIIAqVI2KE.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/7I6VUdPj6tQECNHdviJkUHD2u89.jpg",
            "video_url": "https://www.youtube.com/watch?v=qEVUqWsJtJA",
            "rating": 9.0,
            "release_year": 2023,
            "language": "English",
            "duration": "2h 49m",
            "cast": "Keanu Reeves, Donnie Yen, Bill Skarsgård, Laurence Fishburne, Ian McShane",
            "crew": "Director: Chad Stahelski",
            "parent": jw_parent,
            "part_number": 4,
            "part_name": "Chapter 4"
        },
        genre_slugs=['action', 'thriller']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'John Wick: Chapter 4' not found in DB")

# -------------------------------------------------------
# 3. The Godfather Trilogy
# -------------------------------------------------------
print("\n--- The Godfather Trilogy ---")
try:
    gf_parent = Movie.objects.get(title="The Godfather")
    gf_parent.title = "The Godfather Trilogy"
    gf_parent.duration = "3 Movies"
    gf_parent.description = "The epic saga of the Corleone crime family, spanning decades of power, betrayal, and the dark cost of the American Dream."
    gf_parent.release_year = 1990
    gf_parent.save()
    print(f"  Updated parent: The Godfather Trilogy")

    upsert_movie(
        title="The Godfather",
        defaults={
            "description": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
            "video_url": "https://www.youtube.com/watch?v=UaVTIH8mujA",
            "rating": 9.8,
            "release_year": 1972,
            "language": "English",
            "duration": "2h 55m",
            "cast": "Marlon Brando, Al Pacino, James Caan, Robert Duvall, Diane Keaton",
            "crew": "Director: Francis Ford Coppola",
            "parent": gf_parent,
            "part_number": 1,
            "part_name": "The Godfather"
        },
        genre_slugs=['crime', 'drama']
    )

    upsert_movie(
        title="The Godfather Part II",
        defaults={
            "description": "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/kGzFbGhp99zva6oZODW5atUtnqi.jpg",
            "video_url": "https://www.youtube.com/watch?v=9O1Iy9od7-A",
            "rating": 9.7,
            "release_year": 1974,
            "language": "English",
            "duration": "3h 22m",
            "cast": "Al Pacino, Robert De Niro, Robert Duvall, Diane Keaton, John Cazale",
            "crew": "Director: Francis Ford Coppola",
            "parent": gf_parent,
            "part_number": 2,
            "part_name": "Part II"
        },
        genre_slugs=['crime', 'drama']
    )

    upsert_movie(
        title="The Godfather Part III",
        defaults={
            "description": "In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don Michael Corleone seeks to vow for his sins while taking a young protégé under his wing.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/lm3pQ2QoQ16pextRsmnUbG2onES.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/eGnpMWezENkmLSa1jbu1GuPC4xh.jpg",
            "video_url": "https://www.youtube.com/watch?v=c2G2Kmt_oM4",
            "rating": 8.5,
            "release_year": 1990,
            "language": "English",
            "duration": "2h 42m",
            "cast": "Al Pacino, Diane Keaton, Andy Garcia, Talia Shire, Sofia Coppola",
            "crew": "Director: Francis Ford Coppola",
            "parent": gf_parent,
            "part_number": 3,
            "part_name": "Part III"
        },
        genre_slugs=['crime', 'drama']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'The Godfather' not found in DB")

# -------------------------------------------------------
# 4. The Matrix Collection
# -------------------------------------------------------
print("\n--- The Matrix Collection ---")
try:
    mx_parent = Movie.objects.get(title="The Matrix")
    mx_parent.title = "The Matrix Collection"
    mx_parent.duration = "4 Movies"
    mx_parent.description = "The visionary sci-fi saga exploring the nature of reality, where a computer hacker discovers that all of humanity lives inside a simulated world created by machines."
    mx_parent.release_year = 2021
    mx_parent.save()
    print(f"  Updated parent: The Matrix Collection")

    upsert_movie(
        title="The Matrix",
        defaults={
            "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth -- the life he knows is the elaborate deception of an evil cyber-intelligence.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg",
            "video_url": "https://www.youtube.com/watch?v=vKQi3bBA1y8",
            "rating": 9.5,
            "release_year": 1999,
            "language": "English",
            "duration": "2h 16m",
            "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
            "crew": "Directors: Lana Wachowski, Lilly Wachowski",
            "parent": mx_parent,
            "part_number": 1,
            "part_name": "The Matrix"
        },
        genre_slugs=['action', 'sci-fi']
    )

    upsert_movie(
        title="The Matrix Reloaded",
        defaults={
            "description": "Freedom fighters Neo, Trinity and Morpheus continue to lead the revolt against the Machine Army, unleashing their arsenal of extraordinary skills and weaponry against the systematic forces of repression and exploitation.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/9TGHDvWrqKBzwDxDSrKdtPiFMFh.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/pdVHUsb2eEz9ALNTr6wfRMm6Ihf.jpg",
            "video_url": "https://www.youtube.com/watch?v=kYzz0FSgpSU",
            "rating": 8.5,
            "release_year": 2003,
            "language": "English",
            "duration": "2h 18m",
            "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, Jada Pinkett Smith",
            "crew": "Directors: Lana Wachowski, Lilly Wachowski",
            "parent": mx_parent,
            "part_number": 2,
            "part_name": "Reloaded"
        },
        genre_slugs=['action', 'sci-fi']
    )

    upsert_movie(
        title="The Matrix Revolutions",
        defaults={
            "description": "The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also combating the rogue combatant Agent Smith.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/t1wm4PgOQ8e4z1C6tk1XIpseyFt.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/pdVHUsb2eEz9ALNTr6wfRMm6Ihf.jpg",
            "video_url": "https://www.youtube.com/watch?v=hMbexEPAOQI",
            "rating": 8.2,
            "release_year": 2003,
            "language": "English",
            "duration": "2h 9m",
            "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, Jada Pinkett Smith",
            "crew": "Directors: Lana Wachowski, Lilly Wachowski",
            "parent": mx_parent,
            "part_number": 3,
            "part_name": "Revolutions"
        },
        genre_slugs=['action', 'sci-fi']
    )

    upsert_movie(
        title="The Matrix Resurrections",
        defaults={
            "description": "Return to a world of two realities: one, everyday life; the other, what lies behind it. To find out if his reality is a construct, to truly know himself, Mr. Anderson will have to choose to follow the white rabbit once more.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/8c4a8kE7PizaGQQnditMmI1xbRp.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/eNI7PtK6DEYgZmHWP9gQNuff8pv.jpg",
            "video_url": "https://www.youtube.com/watch?v=9ix7TUGVYIo",
            "rating": 7.8,
            "release_year": 2021,
            "language": "English",
            "duration": "2h 28m",
            "cast": "Keanu Reeves, Carrie-Anne Moss, Yahya Abdul-Mateen II, Jessica Henwick, Jonathan Groff",
            "crew": "Director: Lana Wachowski",
            "parent": mx_parent,
            "part_number": 4,
            "part_name": "Resurrections"
        },
        genre_slugs=['action', 'sci-fi']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'The Matrix' not found in DB")

# -------------------------------------------------------
# 5. A Quiet Place Collection
# -------------------------------------------------------
print("\n--- A Quiet Place Collection ---")
try:
    aqp_parent = Movie.objects.get(title="A Quiet Place")
    aqp_parent.title = "A Quiet Place Collection"
    aqp_parent.duration = "3 Movies"
    aqp_parent.description = "A gripping horror franchise where humanity must survive in silence against creatures that hunt by sound."
    aqp_parent.release_year = 2024
    aqp_parent.save()
    print(f"  Updated parent: A Quiet Place Collection")

    upsert_movie(
        title="A Quiet Place",
        defaults={
            "description": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/nAU74GmpUk7t5iklEp3bufwDq4n.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/roYyPiQDQKmIKUEhO912MOGHTLG.jpg",
            "video_url": "https://www.youtube.com/watch?v=WR7cc5t7tv8",
            "rating": 8.7,
            "release_year": 2018,
            "language": "English",
            "duration": "1h 30m",
            "cast": "Emily Blunt, John Krasinski, Millicent Simmonds, Noah Jupe",
            "crew": "Director: John Krasinski",
            "parent": aqp_parent,
            "part_number": 1,
            "part_name": "A Quiet Place"
        },
        genre_slugs=['horror', 'thriller', 'sci-fi']
    )

    upsert_movie(
        title="A Quiet Place Part II",
        defaults={
            "description": "Following the deadly events at home, the Abbott family must now face the terrors of the outside world as they continue their fight for survival in silence.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/4q2hz2m8hubgvijz8Ez0T2Os2Yv.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/z2UtGA1WggESspi6KOXeo66lvLx.jpg",
            "video_url": "https://www.youtube.com/watch?v=BpdDN9d9Jio",
            "rating": 8.5,
            "release_year": 2021,
            "language": "English",
            "duration": "1h 37m",
            "cast": "Emily Blunt, Cillian Murphy, Millicent Simmonds, Noah Jupe, Djimon Hounsou",
            "crew": "Director: John Krasinski",
            "parent": aqp_parent,
            "part_number": 2,
            "part_name": "Part II"
        },
        genre_slugs=['horror', 'thriller', 'sci-fi']
    )

    upsert_movie(
        title="A Quiet Place: Day One",
        defaults={
            "description": "Experience the day the world went quiet. A woman named Sam finds herself trapped in New York City during the early stages of an invasion by alien creatures who hunt by sound.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/hU42CRk14JuPEdqZG3AWmagiPAq.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/2RVcJbWFmICRDsVxRI8F5xRmRsK.jpg",
            "video_url": "https://www.youtube.com/watch?v=YPY7J-flzE8",
            "rating": 8.3,
            "release_year": 2024,
            "language": "English",
            "duration": "1h 39m",
            "cast": "Lupita Nyong'o, Joseph Quinn, Alex Wolff, Djimon Hounsou",
            "crew": "Director: Michael Sarnoski",
            "parent": aqp_parent,
            "part_number": 3,
            "part_name": "Day One"
        },
        genre_slugs=['horror', 'thriller', 'sci-fi']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'A Quiet Place' not found in DB")

# -------------------------------------------------------
# 6. It Collection
# -------------------------------------------------------
print("\n--- It Collection ---")
try:
    it_parent = Movie.objects.get(title="It")
    it_parent.title = "It Collection"
    it_parent.duration = "2 Movies"
    it_parent.description = "Stephen King's terrifying tale of Pennywise the Dancing Clown, a shape-shifting evil that preys on the children of Derry, Maine every 27 years."
    it_parent.release_year = 2019
    it_parent.save()
    print(f"  Updated parent: It Collection")

    upsert_movie(
        title="It",
        defaults={
            "description": "In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of Derry, their small Maine town.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/9E2y5Q7WlCVNEhP5GiVTjhEhx1o.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/tcheoA2nPATCm2vvXw2newjHsBa.jpg",
            "video_url": "https://www.youtube.com/watch?v=FnCdOQs95i8",
            "rating": 8.7,
            "release_year": 2017,
            "language": "English",
            "duration": "2h 15m",
            "cast": "Bill Skarsgård, Jaeden Martell, Finn Wolfhard, Sophia Lillis, Jack Dylan Grazer",
            "crew": "Director: Andy Muschietti",
            "parent": it_parent,
            "part_number": 1,
            "part_name": "Chapter One"
        },
        genre_slugs=['horror', 'thriller']
    )

    upsert_movie(
        title="It Chapter Two",
        defaults={
            "description": "Twenty-seven years after their first encounter with the terrifying Pennywise, the Losers Club have grown up and moved away, until a devastating phone call brings them back.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/zfE0R94v1E8cuKAerbskfD3VfUt.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/8miCtHbHSJJqBMIqh6MAfZjkfMP.jpg",
            "video_url": "https://www.youtube.com/watch?v=xhJ5P7Up3jA",
            "rating": 8.3,
            "release_year": 2019,
            "language": "English",
            "duration": "2h 49m",
            "cast": "Jessica Chastain, James McAvoy, Bill Hader, Bill Skarsgård, Isaiah Mustafa",
            "crew": "Director: Andy Muschietti",
            "parent": it_parent,
            "part_number": 2,
            "part_name": "Chapter Two"
        },
        genre_slugs=['horror', 'thriller']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'It' not found in DB")

# -------------------------------------------------------
# 7. Blade Runner Collection
# -------------------------------------------------------
print("\n--- Blade Runner Collection ---")
try:
    br_parent = Movie.objects.get(title="Blade Runner 2049")
    br_parent.title = "Blade Runner Collection"
    br_parent.duration = "2 Movies"
    br_parent.description = "The visionary sci-fi saga exploring what it means to be human in a dystopian future where bioengineered beings walk among us."
    br_parent.release_year = 2017
    br_parent.save()
    print(f"  Updated parent: Blade Runner Collection")

    upsert_movie(
        title="Blade Runner",
        defaults={
            "description": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/63N9uy8nd9j7Eog2axPQ8lbr3Wj.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/sC4Dpmn87oz3AcBRkNH5VhDlBjh.jpg",
            "video_url": "https://www.youtube.com/watch?v=eogpIG53Cis",
            "rating": 9.0,
            "release_year": 1982,
            "language": "English",
            "duration": "1h 57m",
            "cast": "Harrison Ford, Rutger Hauer, Sean Young, Daryl Hannah, Edward James Olmos",
            "crew": "Director: Ridley Scott",
            "parent": br_parent,
            "part_number": 1,
            "part_name": "Blade Runner"
        },
        genre_slugs=['sci-fi', 'thriller', 'drama']
    )

    upsert_movie(
        title="Blade Runner 2049",
        defaults={
            "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/sAtoMqDVhNDQBc3QJL3RF6hlhGq.jpg",
            "video_url": "https://www.youtube.com/watch?v=gCcx85zbxz4",
            "rating": 9.2,
            "release_year": 2017,
            "language": "English",
            "duration": "2h 44m",
            "cast": "Ryan Gosling, Harrison Ford, Ana de Armas, Jared Leto, Robin Wright",
            "crew": "Director: Denis Villeneuve",
            "parent": br_parent,
            "part_number": 2,
            "part_name": "2049"
        },
        genre_slugs=['sci-fi', 'thriller', 'drama']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'Blade Runner 2049' not found in DB")

# -------------------------------------------------------
# 8. Gladiator Collection
# -------------------------------------------------------
print("\n--- Gladiator Collection ---")
try:
    glad_parent = Movie.objects.get(title="Gladiator")
    glad_parent.title = "Gladiator Collection"
    glad_parent.duration = "2 Movies"
    glad_parent.description = "Ridley Scott's epic saga of vengeance, honor, and glory in ancient Rome — spanning generations of warriors who defy emperors in the Colosseum."
    glad_parent.release_year = 2024
    glad_parent.save()
    print(f"  Updated parent: Gladiator Collection")

    upsert_movie(
        title="Gladiator",
        defaults={
            "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/ty8hDCccv7Jzzq3t5ikLExRqySg.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/hND3gfvni4eoVfvJcuZ9qyUFqhm.jpg",
            "video_url": "https://www.youtube.com/watch?v=P5ieIbInFpg",
            "rating": 9.5,
            "release_year": 2000,
            "language": "English",
            "duration": "2h 35m",
            "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed, Richard Harris",
            "crew": "Director: Ridley Scott",
            "parent": glad_parent,
            "part_number": 1,
            "part_name": "Gladiator"
        },
        genre_slugs=['action', 'drama', 'adventure']
    )

    upsert_movie(
        title="Gladiator II",
        defaults={
            "description": "Lucius, the former heir to the Roman Empire, is forced into the Colosseum after his home is conquered. With rage in his heart and the future of the Empire at stake, he must fight to return the glory of Rome to its people.",
            "content_type": "movie",
            "poster_url": "https://image.tmdb.org/t/p/original/2cxhvwyEg95dBMr8NjC0YlYJ1VR.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/iFbQjk3Xa2Jjn6gUcHCrwB0MCM.jpg",
            "video_url": "https://www.youtube.com/watch?v=4rgYUipGJNo",
            "rating": 8.8,
            "release_year": 2024,
            "language": "English",
            "duration": "2h 28m",
            "cast": "Paul Mescal, Pedro Pascal, Denzel Washington, Connie Nielsen, Joseph Quinn",
            "crew": "Director: Ridley Scott",
            "parent": glad_parent,
            "part_number": 2,
            "part_name": "Gladiator II"
        },
        genre_slugs=['action', 'drama', 'adventure']
    )
except Movie.DoesNotExist:
    print("  SKIP: 'Gladiator' not found in DB")


# ============================================================
# TV SERIES SEASONS
# ============================================================

# -------------------------------------------------------
# 8. Breaking Bad - 5 Seasons
# -------------------------------------------------------
print("\n--- Breaking Bad Seasons ---")
try:
    bb_parent = Movie.objects.get(title="Breaking Bad")
    bb_parent.duration = "5 Seasons"
    bb_parent.save()

    bb_seasons = [
        {
            "title": "Breaking Bad: Season 1",
            "description": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine to secure his family's future.",
            "release_year": 2008,
            "duration": "7 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Betsy Brandt",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.0,
        },
        {
            "title": "Breaking Bad: Season 2",
            "description": "Walt and Jesse realize how dire their situation has become. They must deal with new and unexpected problems, while trying to keep their meth business going.",
            "release_year": 2009,
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Bob Odenkirk",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.2,
        },
        {
            "title": "Breaking Bad: Season 3",
            "description": "Walt continues to spiral deeper into the drug world while Jesse tries to get clean. Gus Fring enters the picture as a major player in the meth trade.",
            "release_year": 2010,
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Giancarlo Esposito",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.4,
        },
        {
            "title": "Breaking Bad: Season 4",
            "description": "As Walt deals with the aftermath of his confrontation with Gus, the DEA continues its investigation, and Jesse struggles with his own moral compass.",
            "release_year": 2011,
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Giancarlo Esposito",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.6,
        },
        {
            "title": "Breaking Bad: Season 5",
            "description": "Walt's empire grows and the consequences of his choices come crashing down on everyone he knows, leading to one of the most intense and satisfying finales in television history.",
            "release_year": 2013,
            "duration": "16 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Bob Odenkirk, Jesse Plemons",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.8,
        },
    ]

    for i, s in enumerate(bb_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": bb_parent.poster_url,
                "banner_url": bb_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "English",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creator: Vince Gilligan",
                "parent": bb_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['crime', 'drama', 'thriller']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Breaking Bad' not found in DB")

# -------------------------------------------------------
# 9. The Boys - 4 Seasons
# -------------------------------------------------------
print("\n--- The Boys Seasons ---")
try:
    boys_parent = Movie.objects.get(title="The Boys")
    boys_parent.duration = "4 Seasons"
    boys_parent.save()

    boys_seasons = [
        {
            "title": "The Boys: Season 1",
            "description": "A group of vigilantes set out to take down corrupt superheroes who abuse their superpowers. Hughie joins the group after his girlfriend is killed by a superhero.",
            "release_year": 2019,
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Dominique McElligott",
            "video_url": "https://www.youtube.com/watch?v=M1BHuPScwbg",
            "rating": 9.0,
        },
        {
            "title": "The Boys: Season 2",
            "description": "The Boys are on the run from the law, hunted by the Supes, and desperately trying to regroup and fight back against Vought. Meanwhile, Stormfront enters the picture.",
            "release_year": 2020,
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Aya Cash",
            "video_url": "https://www.youtube.com/watch?v=M1BHuPScwbg",
            "rating": 9.2,
        },
        {
            "title": "The Boys: Season 3",
            "description": "The Boys search for a weapon to use against the Supes while Homelander becomes increasingly unstable. The introduction of Soldier Boy changes everything.",
            "release_year": 2022,
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Jensen Ackles, Erin Moriarty",
            "video_url": "https://www.youtube.com/watch?v=M1BHuPScwbg",
            "rating": 9.3,
        },
        {
            "title": "The Boys: Season 4",
            "description": "As Homelander tightens his grip and Victoria Neuman inches closer to the Oval Office, The Boys are more desperate than ever to stop the corrupt Supes before it's too late.",
            "release_year": 2024,
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Cameron Crovetti",
            "video_url": "https://www.youtube.com/watch?v=M1BHuPScwbg",
            "rating": 9.1,
        },
    ]

    for i, s in enumerate(boys_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": boys_parent.poster_url,
                "banner_url": boys_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "English",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creator: Eric Kripke",
                "parent": boys_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['action', 'sci-fi', 'drama']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'The Boys' not found in DB")

# -------------------------------------------------------
# 10. Wednesday - 2 Seasons
# -------------------------------------------------------
print("\n--- Wednesday Seasons ---")
try:
    wed_parent = Movie.objects.get(title="Wednesday")
    wed_parent.duration = "2 Seasons"
    wed_parent.save()

    wed_seasons = [
        {
            "title": "Wednesday: Season 1",
            "description": "Follows Wednesday Addams' years as a student at Nevermore Academy, where she attempts to master her emerging psychic ability, thwart a monstrous killing spree, and solve the supernatural mystery that embroiled her parents 25 years ago.",
            "release_year": 2022,
            "duration": "8 Episodes",
            "cast": "Jenna Ortega, Gwendoline Christie, Riki Lindhome, Jamie McShane, Catherine Zeta-Jones",
            "video_url": "https://www.youtube.com/watch?v=Di310WS8zLk",
            "rating": 8.9,
        },
        {
            "title": "Wednesday: Season 2",
            "description": "Wednesday returns to Nevermore Academy with new mysteries to solve and darker threats lurking. As she delves deeper into the supernatural world, alliances shift and new enemies emerge.",
            "release_year": 2025,
            "duration": "8 Episodes",
            "cast": "Jenna Ortega, Catherine Zeta-Jones, Steve Buscemi, Christopher Lloyd, Joanna Lumley",
            "video_url": "https://www.youtube.com/watch?v=Di310WS8zLk",
            "rating": 8.8,
        },
    ]

    for i, s in enumerate(wed_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": wed_parent.poster_url,
                "banner_url": wed_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "English",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creators: Alfred Gough, Miles Millar",
                "parent": wed_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['comedy', 'mystery', 'horror']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Wednesday' not found in DB")

# -------------------------------------------------------
# 11. The Last of Us - 2 Seasons
# -------------------------------------------------------
print("\n--- The Last of Us Seasons ---")
try:
    tlou_parent = Movie.objects.get(title="The Last of Us")
    tlou_parent.duration = "2 Seasons"
    tlou_parent.save()

    tlou_seasons = [
        {
            "title": "The Last of Us: Season 1",
            "description": "After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl who may be humanity's last hope. Together, they journey across a devastated America.",
            "release_year": 2023,
            "duration": "9 Episodes",
            "cast": "Pedro Pascal, Bella Ramsey, Anna Torv, Gabriel Luna, Merle Dandridge",
            "video_url": "https://www.youtube.com/watch?v=uLtkt8BonwM",
            "rating": 9.3,
        },
        {
            "title": "The Last of Us: Season 2",
            "description": "Five years after the events at the hospital, Joel and Ellie's bond is tested as the consequences of Joel's choice catch up with them. New threats and moral dilemmas force them apart.",
            "release_year": 2025,
            "duration": "7 Episodes",
            "cast": "Pedro Pascal, Bella Ramsey, Kaitlyn Dever, Isabela Merced, Young Mazino",
            "video_url": "https://www.youtube.com/watch?v=uLtkt8BonwM",
            "rating": 9.1,
        },
    ]

    for i, s in enumerate(tlou_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": tlou_parent.poster_url,
                "banner_url": tlou_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "English",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creators: Craig Mazin, Neil Druckmann",
                "parent": tlou_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['drama', 'action', 'horror']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'The Last of Us' not found in DB")

# -------------------------------------------------------
# 12. Squid Game - 2 Seasons
# -------------------------------------------------------
print("\n--- Squid Game Seasons ---")
try:
    sg_parent = Movie.objects.get(title="Squid Game")
    sg_parent.duration = "2 Seasons"
    sg_parent.save()

    sg_seasons = [
        {
            "title": "Squid Game: Season 1",
            "description": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes: a survival game that has a whopping 45.6 billion-won prize at stake.",
            "release_year": 2021,
            "duration": "9 Episodes",
            "cast": "Lee Jung-jae, Park Hae-soo, Wi Ha-joon, HoYeon Jung, O Yeong-su",
            "video_url": "https://www.youtube.com/watch?v=oqxAJKy0ii4",
            "rating": 9.2,
        },
        {
            "title": "Squid Game: Season 2",
            "description": "Three years after winning Squid Game, Player 456 gave up going to the States and returns with a new resolution in his mind. Gi-hun once again dives into the mysterious survival game.",
            "release_year": 2024,
            "duration": "7 Episodes",
            "cast": "Lee Jung-jae, Lee Byung-hun, Wi Ha-joon, Gong Yoo, Yim Si-wan",
            "video_url": "https://www.youtube.com/watch?v=oqxAJKy0ii4",
            "rating": 8.8,
        },
    ]

    for i, s in enumerate(sg_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": sg_parent.poster_url,
                "banner_url": sg_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "Korean",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creator: Hwang Dong-hyuk",
                "parent": sg_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['thriller', 'drama', 'action']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Squid Game' not found in DB")

# -------------------------------------------------------
# 13. Dark - 3 Seasons
# -------------------------------------------------------
print("\n--- Dark Seasons ---")
try:
    dark_parent = Movie.objects.get(title="Dark")
    dark_parent.duration = "3 Seasons"
    dark_parent.save()

    dark_seasons = [
        {
            "title": "Dark: Season 1",
            "description": "A children's disappearance sets four families on a frantic hunt for answers as they unearth a mind-bending mystery that spans three generations in the small German town of Winden.",
            "release_year": 2017,
            "duration": "10 Episodes",
            "cast": "Louis Hofmann, Oliver Masucci, Jördis Triebel, Maja Schöne, Lisa Vicari",
            "video_url": "https://www.youtube.com/watch?v=rrwyCJ08qFM",
            "rating": 9.3,
        },
        {
            "title": "Dark: Season 2",
            "description": "Jonas travels to 2052, while Claudia, Noah, and the Stranger try to change the future. The mystery deepens as new connections between the past and future are revealed.",
            "release_year": 2019,
            "duration": "8 Episodes",
            "cast": "Louis Hofmann, Oliver Masucci, Jördis Triebel, Andreas Pietschmann, Maja Schöne",
            "video_url": "https://www.youtube.com/watch?v=rrwyCJ08qFM",
            "rating": 9.5,
        },
        {
            "title": "Dark: Season 3",
            "description": "The final cycle begins. In the last season, the question is not where or when — but which world. Jonas and Martha fight for the survival of their world.",
            "release_year": 2020,
            "duration": "8 Episodes",
            "cast": "Louis Hofmann, Lisa Vicari, Oliver Masucci, Andreas Pietschmann, Maja Schöne",
            "video_url": "https://www.youtube.com/watch?v=rrwyCJ08qFM",
            "rating": 9.4,
        },
    ]

    for i, s in enumerate(dark_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": dark_parent.poster_url,
                "banner_url": dark_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "German",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creators: Baran bo Odar, Jantje Friese",
                "parent": dark_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['sci-fi', 'thriller', 'mystery']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Dark' not found in DB")

# -------------------------------------------------------
# 14. The Family Man - 2 Seasons
# -------------------------------------------------------
print("\n--- The Family Man Seasons ---")
try:
    fm_parent = Movie.objects.get(title="The Family Man")
    fm_parent.duration = "2 Seasons"
    fm_parent.save()

    fm_seasons = [
        {
            "title": "The Family Man: Season 1",
            "description": "Srikant Tiwari is a middle-class man who also secretly works as an intelligence officer for the Threat Analysis and Surveillance Cell (TASC). He tries to balance his family life with his dangerous job.",
            "release_year": 2019,
            "duration": "10 Episodes",
            "cast": "Manoj Bajpayee, Priyamani, Sharib Hashmi, Neeraj Madhav, Gul Panag",
            "video_url": "https://www.youtube.com/watch?v=bv9xrcqcMys",
            "rating": 9.2,
        },
        {
            "title": "The Family Man: Season 2",
            "description": "Srikant Tiwari is pitted against a new, deadlier nemesis Raji, and must race against time to prevent a catastrophic attack while his personal life crumbles around him.",
            "release_year": 2021,
            "duration": "9 Episodes",
            "cast": "Manoj Bajpayee, Samantha Ruth Prabhu, Priyamani, Sharib Hashmi",
            "video_url": "https://www.youtube.com/watch?v=bv9xrcqcMys",
            "rating": 9.4,
        },
    ]

    for i, s in enumerate(fm_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": fm_parent.poster_url,
                "banner_url": fm_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "Hindi",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creators: Raj Nidimoru, Krishna D.K.",
                "parent": fm_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['action', 'thriller', 'drama']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'The Family Man' not found in DB")

# -------------------------------------------------------
# 15. Asur - 2 Seasons
# -------------------------------------------------------
print("\n--- Asur Seasons ---")
try:
    asur_parent = Movie.objects.get(title="Asur: Welcome to Your Dark Side")
    asur_parent.duration = "2 Seasons"
    asur_parent.save()

    asur_seasons = [
        {
            "title": "Asur: Season 1",
            "description": "A forensic expert and a judicial officer join forces to investigate a series of ritualistic murders linked to Indian mythology. The hunt leads them into the darkest corners of the human psyche.",
            "release_year": 2020,
            "duration": "8 Episodes",
            "cast": "Arshad Warsi, Barun Sobti, Anupriya Goenka, Ridhi Dogra, Pawan Chopra",
            "video_url": "https://www.youtube.com/watch?v=9AZnfGUnPZB",
            "rating": 9.0,
        },
        {
            "title": "Asur: Season 2",
            "description": "The dark saga continues as Dhananjay and Nikhil face an even more sinister serial killer who challenges them with elaborate mythological puzzles. The stakes are higher than ever.",
            "release_year": 2023,
            "duration": "8 Episodes",
            "cast": "Arshad Warsi, Barun Sobti, Anupriya Goenka, Ridhi Dogra, Meiyang Chang",
            "video_url": "https://www.youtube.com/watch?v=9AZnfGUnPZB",
            "rating": 8.8,
        },
    ]

    for i, s in enumerate(asur_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": asur_parent.poster_url,
                "banner_url": asur_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "Hindi",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creator: Gaurav Shukla",
                "parent": asur_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['thriller', 'mystery', 'crime']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Asur' not found in DB")

# -------------------------------------------------------
# 16. Alice in Borderland - 2 Seasons
# -------------------------------------------------------
print("\n--- Alice in Borderland Seasons ---")
try:
    aib_parent = Movie.objects.get(title="Alice in the Borderland")
    aib_parent.duration = "2 Seasons"
    aib_parent.save()

    aib_seasons = [
        {
            "title": "Alice in the Borderland: Season 1",
            "description": "A group of bored, directionless young men are transported to a parallel dimension where they must compete in dangerous games to survive, each with a playing card difficulty level.",
            "release_year": 2020,
            "duration": "8 Episodes",
            "cast": "Kento Yamazaki, Tao Tsuchiya, Nijiro Murakami, Yuki Morinaga, Keita Machida",
            "video_url": "https://www.youtube.com/watch?v=49_44FFKZ1M",
            "rating": 8.8,
        },
        {
            "title": "Alice in the Borderland: Season 2",
            "description": "Arisu and Usagi continue their quest to return to the real world by clearing the remaining face card games, facing their most dangerous opponents yet.",
            "release_year": 2022,
            "duration": "8 Episodes",
            "cast": "Kento Yamazaki, Tao Tsuchiya, Nijiro Murakami, Riisa Naka, Yuri Tsunematsu",
            "video_url": "https://www.youtube.com/watch?v=49_44FFKZ1M",
            "rating": 9.0,
        },
    ]

    for i, s in enumerate(aib_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": aib_parent.poster_url,
                "banner_url": aib_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "Japanese",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Director: Shinsuke Sato",
                "parent": aib_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['thriller', 'sci-fi', 'mystery']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'Alice in the Borderland' not found in DB")

# -------------------------------------------------------
# 17. From - 3 Seasons
# -------------------------------------------------------
print("\n--- From Seasons ---")
try:
    from_parent = Movie.objects.get(title="From")
    from_parent.duration = "3 Seasons"
    from_parent.save()

    from_seasons = [
        {
            "title": "From: Season 1",
            "description": "Unravel the mystery of a nightmarish town in middle America that traps all those who enter. As the residents struggle to maintain a sense of normalcy, they must also survive the creatures that come out at night.",
            "release_year": 2022,
            "duration": "10 Episodes",
            "cast": "Harold Perrineau, Catalina Sandino Moreno, Eion Bailey, David Alpay, Elizabeth Saunders",
            "video_url": "https://www.youtube.com/watch?v=pDHqAj4eJcM",
            "rating": 8.7,
        },
        {
            "title": "From: Season 2",
            "description": "Hidden truths about the nature and terrifying history of the town begin to emerge, even as life for its residents continues to be a terrifying mystery.",
            "release_year": 2023,
            "duration": "10 Episodes",
            "cast": "Harold Perrineau, Catalina Sandino Moreno, Eion Bailey, Scott McCord, Robert Joy",
            "video_url": "https://www.youtube.com/watch?v=pDHqAj4eJcM",
            "rating": 8.9,
        },
        {
            "title": "From: Season 3",
            "description": "The township grapples with impossible questions and unimaginable horror as the residents fight to break free while the creatures' true nature begins to reveal itself.",
            "release_year": 2025,
            "duration": "10 Episodes",
            "cast": "Harold Perrineau, Catalina Sandino Moreno, Eion Bailey, Robert Joy, Hannah Cheramy",
            "video_url": "https://www.youtube.com/watch?v=pDHqAj4eJcM",
            "rating": 9.0,
        },
    ]

    for i, s in enumerate(from_seasons, 1):
        upsert_movie(
            title=s["title"],
            defaults={
                "description": s["description"],
                "content_type": "series",
                "poster_url": from_parent.poster_url,
                "banner_url": from_parent.banner_url,
                "video_url": s["video_url"],
                "rating": s["rating"],
                "release_year": s["release_year"],
                "language": "English",
                "duration": s["duration"],
                "cast": s["cast"],
                "crew": "Creator: John Griffin",
                "parent": from_parent,
                "part_number": i,
                "part_name": f"Season {i}"
            },
            genre_slugs=['horror', 'mystery', 'thriller']
        )
except Movie.DoesNotExist:
    print("  SKIP: 'From' not found in DB")

print("\n[DONE] All series seasons and movie sequels seeding completed successfully!")
