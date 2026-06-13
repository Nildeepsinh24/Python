import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()

from cine_verse.models import Genre, Movie

print("Connected to database:", django.db.connection.settings_dict['NAME'])

# Helper to retrieve parent genre objects
def get_genres_for_slugs(slugs):
    return list(Genre.objects.filter(slug__in=slugs))

# Helper to upsert a season
def upsert_season(title, parent, part_number, defaults, genre_slugs):
    defaults['parent'] = parent
    defaults['part_number'] = part_number
    defaults['content_type'] = 'series'
    
    movie, created = Movie.objects.get_or_create(
        title=title,
        parent=parent,
        part_number=part_number,
        defaults=defaults
    )
    
    if not created:
        print(f"Updating existing season: {title}")
        for k, v in defaults.items():
            setattr(movie, k, v)
        movie.save()
    else:
        print(f"Created new season: {title}")
        
    # Set genres
    genres = get_genres_for_slugs(genre_slugs)
    movie.genres.set(genres)
    return movie

# 1. THE BOYS
try:
    tb_parent = Movie.objects.get(title="The Boys")
    tb_parent.duration = "4 Seasons"
    tb_parent.video_url = "https://www.youtube.com/watch?v=M1BHuPScwbg"
    tb_parent.save()
    
    # Season 1
    upsert_season(
        title="The Boys: Season 1",
        parent=tb_parent,
        part_number=1,
        genre_slugs=['action', 'sci-fi', 'comedy'],
        defaults={
            "description": "A fun, gritty, and dark superhero series focusing on a group of vigilantes set out to take down corrupt superheroes who abuse their superpowers.",
            "poster_url": "https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/bq28ajZaoMyzEIm6REelqyqtEDZ.jpg",
            "video_url": "https://www.youtube.com/watch?v=06apyREy70A",
            "rating": 9.2,
            "release_year": 2019,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Jessie T. Usher",
            "crew": "Creator: Eric Kripke",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="The Boys: Season 2",
        parent=tb_parent,
        part_number=2,
        genre_slugs=['action', 'sci-fi', 'comedy'],
        defaults={
            "description": "The Boys are on the run from the law, hunted by the Supes, and desperately trying to regroup and fight back against Vought.",
            "poster_url": "https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/mGRrB2n17V65Ujnp866EsHQ366R.jpg",
            "video_url": "https://www.youtube.com/watch?v=MN8fFM1ZdWo",
            "rating": 9.3,
            "release_year": 2020,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Dominique McElligott, Aya Cash",
            "crew": "Creator: Eric Kripke",
            "part_name": "Season 2"
        }
    )
    # Season 3
    upsert_season(
        title="The Boys: Season 3",
        parent=tb_parent,
        part_number=3,
        genre_slugs=['action', 'sci-fi', 'comedy'],
        defaults={
            "description": "It's been a year of calm. Homelander's subdued. Butcher works for the government, supervised by Hughie of all people. But both men itch to turn this peace into blood and bone.",
            "poster_url": "https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/21nb1VR26wb7q1S8dWpBY14nshx.jpg",
            "video_url": "https://www.youtube.com/watch?v=K-8VYK5CptU",
            "rating": 9.4,
            "release_year": 2022,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Jensen Ackles",
            "crew": "Creator: Eric Kripke",
            "part_name": "Season 3"
        }
    )
    # Season 4
    upsert_season(
        title="The Boys: Season 4",
        parent=tb_parent,
        part_number=4,
        genre_slugs=['action', 'sci-fi', 'comedy'],
        defaults={
            "description": "The world is on the brink. Victoria Neuman is closer than ever to the Oval Office and under the muscled thumb of Homelander, who is consolidating his power.",
            "poster_url": "https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/bq28ajZaoMyzEIm6REelqyqtEDZ.jpg",
            "video_url": "https://www.youtube.com/watch?v=M1BHuPScwbg",
            "rating": 9.4,
            "release_year": 2024,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Jeffrey Dean Morgan",
            "crew": "Creator: Eric Kripke",
            "part_name": "Season 4"
        }
    )
except Movie.DoesNotExist:
    print("The Boys parent not found.")

# 2. BREAKING BAD
try:
    bb_parent = Movie.objects.get(title="Breaking Bad")
    bb_parent.duration = "5 Seasons"
    bb_parent.video_url = "https://www.youtube.com/watch?v=HhesaQXLuRY"
    bb_parent.save()
    
    # Season 1
    upsert_season(
        title="Breaking Bad: Season 1",
        parent=bb_parent,
        part_number=1,
        genre_slugs=['drama', 'thriller'],
        defaults={
            "description": "Diagnosed with terminal lung cancer, high school chemistry teacher Walter White teams up with former student Jesse Pinkman to manufacture and sell meth.",
            "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg",
            "video_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
            "rating": 9.8,
            "release_year": 2008,
            "language": "English",
            "duration": "7 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, RJ Mitte",
            "crew": "Creator: Vince Gilligan",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="Breaking Bad: Season 2",
        parent=bb_parent,
        part_number=2,
        genre_slugs=['drama', 'thriller'],
        defaults={
            "description": "Walt and Jesse face the harsh realities of drug dealing as their enterprise grows, while dealing with Walt's declining health and family secrets.",
            "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/1m7q9tQxJb9n1q82BqGgX2f7n9d.jpg",
            "video_url": "https://www.youtube.com/watch?v=1SjD2y6rQxU",
            "rating": 9.8,
            "release_year": 2009,
            "language": "English",
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Betsy Brandt, RJ Mitte",
            "crew": "Creator: Vince Gilligan",
            "part_name": "Season 2"
        }
    )
    # Season 3
    upsert_season(
        title="Breaking Bad: Season 3",
        parent=bb_parent,
        part_number=3,
        genre_slugs=['drama', 'thriller'],
        defaults={
            "description": "Walt faces new threats from the Mexican drug cartel and the enigmatic Gus Fring, while his marriage collapses.",
            "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/2m7q9tQxJb9n1q82BqGgX2f7n9d.jpg",
            "video_url": "https://www.youtube.com/watch?v=F1HNu5eK1Yg",
            "rating": 9.9,
            "release_year": 2010,
            "language": "English",
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk, Giancarlo Esposito",
            "crew": "Creator: Vince Gilligan",
            "part_name": "Season 3"
        }
    )
    # Season 4
    upsert_season(
        title="Breaking Bad: Season 4",
        parent=bb_parent,
        part_number=4,
        genre_slugs=['drama', 'thriller'],
        defaults={
            "description": "Walt and Jesse navigate their perilous partnership with Gus Fring, culminating in an all-out battle of wits and survival.",
            "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/3m7q9tQxJb9n1q82BqGgX2f7n9d.jpg",
            "video_url": "https://www.youtube.com/watch?v=UaVTIH8mujA",
            "rating": 9.9,
            "release_year": 2011,
            "language": "English",
            "duration": "13 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk, Giancarlo Esposito, Jonathan Banks",
            "crew": "Creator: Vince Gilligan",
            "part_name": "Season 4"
        }
    )
    # Season 5
    upsert_season(
        title="Breaking Bad: Season 5",
        parent=bb_parent,
        part_number=5,
        genre_slugs=['drama', 'thriller'],
        defaults={
            "description": "Walt takes full control of the meth empire as Heisenberg, leading to a dramatic and destructive conclusion.",
            "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg",
            "video_url": "https://www.youtube.com/watch?v=5NyolbEw3eM",
            "rating": 9.9,
            "release_year": 2012,
            "language": "English",
            "duration": "16 Episodes",
            "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk, Jonathan Banks, Jesse Plemons",
            "crew": "Creator: Vince Gilligan",
            "part_name": "Season 5"
        }
    )
except Movie.DoesNotExist:
    print("Breaking Bad parent not found.")

# 3. THE OFFICE
try:
    to_parent = Movie.objects.get(title="The Office")
    to_parent.duration = "5 Seasons"
    to_parent.video_url = "https://www.youtube.com/watch?v=LHOtME2DLyI"
    to_parent.save()
    
    # Season 1
    upsert_season(
        title="The Office: Season 1",
        parent=to_parent,
        part_number=1,
        genre_slugs=['comedy'],
        defaults={
            "description": "Documentary crew follows the eccentric office manager Michael Scott and his staff at Dunder Mifflin Paper Company.",
            "poster_url": "https://image.tmdb.org/t/p/original/37Uj9foNnZWhgdYS_EcN2Ix8mzi.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/mLyW3UTgi2lsMdtueYODcfAB9Ku.jpg",
            "video_url": "https://www.youtube.com/watch?v=LHOtME2DLyI",
            "rating": 8.8,
            "release_year": 2005,
            "language": "English",
            "duration": "6 Episodes",
            "cast": "Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer, B.J. Novak",
            "crew": "Developer: Greg Daniels",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="The Office: Season 2",
        parent=to_parent,
        part_number=2,
        genre_slugs=['comedy'],
        defaults={
            "description": "Michael continues to cause chaos while Jim and Pam's unspoken romantic tension reaches new heights.",
            "poster_url": "https://image.tmdb.org/t/p/original/37Uj9foNnZWhgdYS_EcN2Ix8mzi.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/mLyW3UTgi2lsMdtueYODcfAB9Ku.jpg",
            "video_url": "https://www.youtube.com/watch?v=gO8N3L_aERg",
            "rating": 9.1,
            "release_year": 2005,
            "language": "English",
            "duration": "22 Episodes",
            "cast": "Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer, B.J. Novak",
            "crew": "Developer: Greg Daniels",
            "part_name": "Season 2"
        }
    )
    # Season 3
    upsert_season(
        title="The Office: Season 3",
        parent=to_parent,
        part_number=3,
        genre_slugs=['comedy'],
        defaults={
            "description": "Jim transfers to the Stamford branch, while Pam calls off her wedding, leading to new dynamics when the branches merge.",
            "poster_url": "https://image.tmdb.org/t/p/original/37Uj9foNnZWhgdYS_EcN2Ix8mzi.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/mLyW3UTgi2lsMdtueYODcfAB9Ku.jpg",
            "video_url": "https://www.youtube.com/watch?v=uK1l0Xm1X2c",
            "rating": 9.2,
            "release_year": 2006,
            "language": "English",
            "duration": "25 Episodes",
            "cast": "Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer, B.J. Novak, Rashida Jones, Ed Helms",
            "crew": "Developer: Greg Daniels",
            "part_name": "Season 3"
        }
    )
except Movie.DoesNotExist:
    print("The Office parent not found.")

# 4. FRIENDS
try:
    fr_parent = Movie.objects.get(title="Friends")
    fr_parent.duration = "3 Seasons"
    fr_parent.video_url = "https://www.youtube.com/watch?v=hDNNmeeJs1Q"
    fr_parent.save()
    
    # Season 1
    upsert_season(
        title="Friends: Season 1",
        parent=fr_parent,
        part_number=1,
        genre_slugs=['comedy'],
        defaults={
            "description": "Six friends living in New York navigate romance, careers, and young adulthood in their twenties.",
            "poster_url": "https://image.tmdb.org/t/p/original/f4FFv3wM5uf6RANFKmIHg7LK6de.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/m3Jev59mJLyUp5bXhY5SVfIBZI0.jpg",
            "video_url": "https://www.youtube.com/watch?v=hDNNmeeJs1Q",
            "rating": 8.9,
            "release_year": 1994,
            "language": "English",
            "duration": "24 Episodes",
            "cast": "Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry, David Schwimmer",
            "crew": "Creators: David Crane, Marta Kauffman",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="Friends: Season 2",
        parent=fr_parent,
        part_number=2,
        genre_slugs=['comedy'],
        defaults={
            "description": "Ross tries to win Rachel over after returning from China, while Joey lands a role on Days of Our Lives.",
            "poster_url": "https://image.tmdb.org/t/p/original/f4FFv3wM5uf6RANFKmIHg7LK6de.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/m3Jev59mJLyUp5bXhY5SVfIBZI0.jpg",
            "video_url": "https://www.youtube.com/watch?v=T_s_7vT1yX0",
            "rating": 9.0,
            "release_year": 1995,
            "language": "English",
            "duration": "24 Episodes",
            "cast": "Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry, David Schwimmer",
            "crew": "Creators: David Crane, Marta Kauffman",
            "part_name": "Season 2"
        }
    )
except Movie.DoesNotExist:
    print("Friends parent not found.")

# 5. WEDNESDAY
try:
    we_parent = Movie.objects.get(title="Wednesday")
    we_parent.duration = "2 Seasons"
    we_parent.video_url = "https://www.youtube.com/watch?v=Di310WS8zLk"
    we_parent.save()
    
    # Season 1
    upsert_season(
        title="Wednesday: Season 1",
        parent=we_parent,
        part_number=1,
        genre_slugs=['comedy', 'horror', 'thriller'],
        defaults={
            "description": "Wednesday Addams investigates a series of supernatural murders at Nevermore Academy while mastering her psychic powers.",
            "poster_url": "https://image.tmdb.org/t/p/original/oOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/iHSwvRVsRyxpX7FE7GbviaDvgGZ.jpg",
            "video_url": "https://www.youtube.com/watch?v=Di310WS8zLk",
            "rating": 8.8,
            "release_year": 2022,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Jenna Ortega, Gwendoline Christie, Riki Lindhome, Emma Myers, Hunter Doohan, Christina Ricci",
            "crew": "Creators: Alfred Gough, Miles Millar",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="Wednesday: Season 2",
        parent=we_parent,
        part_number=2,
        genre_slugs=['comedy', 'horror', 'thriller'],
        defaults={
            "description": "Wednesday returns to Nevermore Academy to face new mysteries, darker secrets, and a sinister stalker.",
            "poster_url": "https://image.tmdb.org/t/p/original/oOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/iHSwvRVsRyxpX7FE7GbviaDvgGZ.jpg",
            "video_url": "https://www.youtube.com/watch?v=9g0Zt6kS8oI",
            "rating": 8.9,
            "release_year": 2025,
            "language": "English",
            "duration": "8 Episodes",
            "cast": "Jenna Ortega, Emma Myers, Joy Sunday, Steve Buscemi",
            "crew": "Creators: Alfred Gough, Miles Millar",
            "part_name": "Season 2"
        }
    )
except Movie.DoesNotExist:
    print("Wednesday parent not found.")

# 6. THE LAST OF US
try:
    tl_parent = Movie.objects.get(title="The Last of Us")
    tl_parent.duration = "2 Seasons"
    tl_parent.video_url = "https://www.youtube.com/watch?v=yQEondeGvKo"
    tl_parent.save()
    
    # Season 1
    upsert_season(
        title="The Last of Us: Season 1",
        parent=tl_parent,
        part_number=1,
        genre_slugs=['drama', 'action'],
        defaults={
            "description": "After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl who may be humanity's last hope.",
            "poster_url": "https://image.tmdb.org/t/p/original/dmo6TYuuJgaYinXBPjrgG9mB5od.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/acevLdSl5I2MK5RYAm7gwAndt1w.jpg",
            "video_url": "https://www.youtube.com/watch?v=uLtkt8BonwM",
            "rating": 9.4,
            "release_year": 2023,
            "language": "English",
            "duration": "9 Episodes",
            "cast": "Pedro Pascal, Bella Ramsey, Gabriel Luna, Anna Torv, Nico Parker",
            "crew": "Creators: Craig Mazin, Neil Druckmann",
            "part_name": "Season 1"
        }
    )
    # Season 2
    upsert_season(
        title="The Last of Us: Season 2",
        parent=tl_parent,
        part_number=2,
        genre_slugs=['drama', 'action'],
        defaults={
            "description": "Five years after their dangerous journey, Joel and Ellie's past catches up to them, leading to new conflicts and challenges.",
            "poster_url": "https://image.tmdb.org/t/p/original/dmo6TYuuJgaYinXBPjrgG9mB5od.jpg",
            "banner_url": "https://image.tmdb.org/t/p/original/acevLdSl5I2MK5RYAm7gwAndt1w.jpg",
            "video_url": "https://www.youtube.com/watch?v=dmo6TYuuJgaY",
            "rating": 9.5,
            "release_year": 2025,
            "language": "English",
            "duration": "7 Episodes",
            "cast": "Pedro Pascal, Bella Ramsey, Kaitlyn Dever, Isabela Merced",
            "crew": "Creators: Craig Mazin, Neil Druckmann",
            "part_name": "Season 2"
        }
    )
except Movie.DoesNotExist:
    print("The Last of Us parent not found.")

print("Seasons seeding completed successfully!")
