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
        print(f"Updating existing movie: {title}")
        for k, v in defaults.items():
            setattr(movie, k, v)
        movie.save()
    else:
        print(f"Created new movie: {title}")
    
    # Add genres
    for g_slug in genre_slugs:
        if g_slug in genres_map:
            movie.genres.add(genres_map[g_slug])
            
    return movie

# 1. Spider-Man Collection
spiderman_parent = upsert_movie(
    title="Spider-Man (MCU) Trilogy",
    defaults={
        "description": "The complete high-stakes journey of Peter Parker in the Marvel Cinematic Universe, balancing high school life with protecting New York.",
        "content_type": "movie",
        "poster_url": "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618",
        "banner_url": "https://image.tmdb.org/t/p/original/tyQo080tijexyUHBvWPwQt26bZa.jpg",
        "video_url": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
        "rating": 9.2,
        "release_year": 2021,
        "language": "English",
        "duration": "3 Movies",
        "is_trending": True,
        "is_popular": True,
        "cast": "Tom Holland, Zendaya, Jacob Batalon",
        "crew": "Director: Jon Watts",
        "display_order": 180
    },
    genre_slugs=['action', 'adventure', 'sci-fi']
)

upsert_movie(
    title="Spider-Man: Homecoming",
    defaults={
        "description": "Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man, and finds himself on the trail of a new menace prowling the skies of New York City.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/45Y6crcltT124S-5Z88gJm3e9a.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/fn4n6metrTfXtD9u5cu7oU7Ifw8.jpg",
        "video_url": "https://www.youtube.com/watch?v=39udgGPyYHI",
        "rating": 8.5,
        "release_year": 2017,
        "language": "English",
        "duration": "2h 13m",
        "cast": "Tom Holland, Michael Keaton, Robert Downey Jr., Zendaya",
        "crew": "Director: Jon Watts",
        "parent": spiderman_parent,
        "part_number": 1,
        "part_name": "Homecoming"
    },
    genre_slugs=['action', 'adventure', 'sci-fi']
)

upsert_movie(
    title="Spider-Man: Far From Home",
    defaults={
        "description": "Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/4q235wzywOU2M4hwvtuiTB0vU7N.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/1Ruzn4VnEw0qYJux4T9Y52TjS0s.jpg",
        "video_url": "https://www.youtube.com/watch?v=Nt9L1jyeSdg",
        "rating": 8.7,
        "release_year": 2019,
        "language": "English",
        "duration": "2h 9m",
        "cast": "Tom Holland, Samuel L. Jackson, Jake Gyllenhaal, Zendaya",
        "crew": "Director: Jon Watts",
        "parent": spiderman_parent,
        "part_number": 2,
        "part_name": "Far From Home"
    },
    genre_slugs=['action', 'adventure', 'sci-fi']
)

upsert_movie(
    title="Spider-Man: No Way Home",
    defaults={
        "description": "Peter Parker's life and reputation are upended when a spell gone wrong opens the multiverse and brings dangerous visitors into his world.",
        "content_type": "movie",
        "poster_url": "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618",
        "banner_url": "https://image.tmdb.org/t/p/original/tyQo080tijexyUHBvWPwQt26bZa.jpg",
        "video_url": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
        "rating": 9.1,
        "release_year": 2021,
        "language": "English",
        "duration": "2h 28m",
        "cast": "Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon",
        "crew": "Director: Jon Watts",
        "parent": spiderman_parent,
        "part_number": 3,
        "part_name": "No Way Home"
    },
    genre_slugs=['action', 'adventure', 'sci-fi']
)

# 2. Dune Collection
dune_parent = upsert_movie(
    title="Dune Collection",
    defaults={
        "description": "The epic saga of Paul Atreides as he navigates the dangerous desert planet of Arrakis and leads the Fremen in a war for the universe.",
        "content_type": "movie",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
        "video_url": "https://www.youtube.com/watch?v=Way9Dexny3w",
        "rating": 9.5,
        "release_year": 2024,
        "language": "English",
        "duration": "2 Movies",
        "is_trending": True,
        "is_popular": True,
        "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Oscar Isaac, Josh Brolin",
        "crew": "Director: Denis Villeneuve",
        "display_order": 20
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

upsert_movie(
    title="Dune: Part One",
    defaults={
        "description": "Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/d5NXSklXkiZt14AL49L4BtZAVXc.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/lz7617S53MIZ9O5qGg7G5617oAb.jpg",
        "video_url": "https://www.youtube.com/watch?v=8g18jFHCLzs",
        "rating": 9.0,
        "release_year": 2021,
        "language": "English",
        "duration": "2h 35m",
        "cast": "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Josh Brolin",
        "crew": "Director: Denis Villeneuve",
        "parent": dune_parent,
        "part_number": 1,
        "part_name": "Part One"
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

upsert_movie(
    title="Dune: Part Two",
    defaults={
        "description": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/czemboc07Bhv5822LqyqtEDZ582.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
        "video_url": "https://www.youtube.com/watch?v=Way9Dexny3w",
        "rating": 9.6,
        "release_year": 2024,
        "language": "English",
        "duration": "2h 46m",
        "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem",
        "crew": "Director: Denis Villeneuve",
        "parent": dune_parent,
        "part_number": 2,
        "part_name": "Part Two"
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

# 3. Avatar Collection
avatar_parent = upsert_movie(
    title="Avatar Collection",
    defaults={
        "description": "Enter the world of Pandora, where a paraplegic Marine embarks on a unique journey of adventure and love, fighting to protect the land he learns to call home.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/kyeqWJfphcuFF0TC0o4lY56u7Ls.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/qnzQm0PCVnSyv1dqpVmRgMWHbLD.jpg",
        "video_url": "https://www.youtube.com/watch?v=d9MyW72ELq0",
        "rating": 9.0,
        "release_year": 2022,
        "language": "English",
        "duration": "2 Movies",
        "is_trending": True,
        "is_popular": True,
        "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang",
        "crew": "Director: James Cameron",
        "display_order": 160
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

upsert_movie(
    title="Avatar",
    defaults={
        "description": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/kyeqWJfphcuFF0TC0o4lY56u7Ls.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/vL526wSBrjSPV67j2RjUuSyjKga.jpg",
        "video_url": "https://www.youtube.com/watch?v=5PSNL1q3fy8",
        "rating": 8.9,
        "release_year": 2009,
        "language": "English",
        "duration": "2h 42m",
        "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang",
        "crew": "Director: James Cameron",
        "parent": avatar_parent,
        "part_number": 1,
        "part_name": "Avatar"
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

upsert_movie(
    title="Avatar: The Way of Water",
    defaults={
        "description": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/uXTg565ahu9RwonCX1V2Hex1NU6.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/qnzQm0PCVnSyv1dqpVmRgMWHbLD.jpg",
        "video_url": "https://www.youtube.com/watch?v=d9MyW72ELq0",
        "rating": 8.7,
        "release_year": 2022,
        "language": "English",
        "duration": "3h 12m",
        "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver, Kate Winslet",
        "crew": "Director: James Cameron",
        "parent": avatar_parent,
        "part_number": 2,
        "part_name": "The Way of Water"
    },
    genre_slugs=['sci-fi', 'adventure', 'action']
)

# 4. Avengers Collection
avengers_parent = upsert_movie(
    title="Avengers Collection",
    defaults={
        "description": "Earth's Mightiest Heroes stand together to battle the threats that no single hero could withstand, culminating in the battle against the Mad Titan, Thanos.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/or7PzF6ZRkJGBlPp6oom5QYQ2yQ.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
        "video_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
        "rating": 9.5,
        "release_year": 2019,
        "language": "English",
        "duration": "4 Movies",
        "is_trending": True,
        "is_popular": True,
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth, Scarlett Johansson",
        "crew": "Directors: Joss Whedon, Anthony Russo, Joe Russo",
        "display_order": 260
    },
    genre_slugs=['action', 'sci-fi', 'adventure']
)

upsert_movie(
    title="The Avengers",
    defaults={
        "description": "Earth's mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/RYMX2wc76YgXeRIyw6d6Z4SAjG.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/9BBTo6m1X2p4d24W2r2kceJ76J8.jpg",
        "video_url": "https://www.youtube.com/watch?v=eOrNdByGMv8",
        "rating": 8.8,
        "release_year": 2012,
        "language": "English",
        "duration": "2h 23m",
        "cast": "Robert Downey Jr., Chris Evans, Scarlett Johansson, Mark Ruffalo",
        "crew": "Director: Joss Whedon",
        "parent": avengers_parent,
        "part_number": 1,
        "part_name": "The Avengers"
    },
    genre_slugs=['action', 'sci-fi', 'adventure']
)

upsert_movie(
    title="Avengers: Age of Ultron",
    defaults={
        "description": "When Tony Stark and Bruce Banner try to jump-start a dormant peacekeeping program called Ultron, things go horribly wrong and it's up to Earth's mightiest heroes to stop the villainous Ultron from enacting his terrible plan.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/4ssDuvj0MKmQki84I2Jrzq5zVaa.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/87Wwquby7w7kZ77t465gA878401.jpg",
        "video_url": "https://www.youtube.com/watch?v=tmeOjFno6Do",
        "rating": 8.5,
        "release_year": 2015,
        "language": "English",
        "duration": "2h 21m",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
        "crew": "Director: Joss Whedon",
        "parent": avengers_parent,
        "part_number": 2,
        "part_name": "Age of Ultron"
    },
    genre_slugs=['action', 'sci-fi', 'adventure']
)

upsert_movie(
    title="Avengers: Infinity War",
    defaults={
        "description": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/7WsyChwLEAx4xdIFqRxyz78V2si.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/bOGkgm7gHn171t4t72nqpj1nPEb.jpg",
        "video_url": "https://www.youtube.com/watch?v=QwievZ1Tx-8",
        "rating": 9.3,
        "release_year": 2018,
        "language": "English",
        "duration": "2h 29m",
        "cast": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans",
        "crew": "Directors: Anthony Russo, Joe Russo",
        "parent": avengers_parent,
        "part_number": 3,
        "part_name": "Infinity War"
    },
    genre_slugs=['action', 'sci-fi', 'adventure']
)

upsert_movie(
    title="Avengers: Endgame",
    defaults={
        "description": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/or7PzF6ZRkJGBlPp6oom5QYQ2yQ.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
        "video_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
        "rating": 9.2,
        "release_year": 2019,
        "language": "English",
        "duration": "3h 01m",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
        "crew": "Directors: Anthony Russo, Joe Russo",
        "parent": avengers_parent,
        "part_number": 4,
        "part_name": "Endgame"
    },
    genre_slugs=['action', 'sci-fi', 'adventure']
)

# 5. The Conjuring Trilogy
conjuring_parent = upsert_movie(
    title="The Conjuring Trilogy",
    defaults={
        "description": "The chilling investigations of paranormal experts Ed and Lorraine Warren as they battle demonic entities and haunted houses.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg",
        "video_url": "https://www.youtube.com/watch?v=k10ETZ42q5o",
        "rating": 8.7,
        "release_year": 2021,
        "language": "English",
        "duration": "3 Movies",
        "is_trending": True,
        "is_popular": True,
        "cast": "Vera Farmiga, Patrick Wilson",
        "crew": "Directors: James Wan, Michael Chaves",
        "display_order": 130
    },
    genre_slugs=['horror', 'thriller']
)

upsert_movie(
    title="The Conjuring",
    defaults={
        "description": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg",
        "video_url": "https://www.youtube.com/watch?v=k10ETZ42q5o",
        "rating": 8.5,
        "release_year": 2013,
        "language": "English",
        "duration": "1h 52m",
        "cast": "Vera Farmiga, Patrick Wilson, Lili Taylor, Ron Livingston",
        "crew": "Director: James Wan",
        "parent": conjuring_parent,
        "part_number": 1,
        "part_name": "The Conjuring"
    },
    genre_slugs=['horror', 'thriller']
)

upsert_movie(
    title="The Conjuring 2",
    defaults={
        "description": "Ed and Lorraine Warren travel to North London to help a single mother raising four children alone in a house plagued by a supernatural spirit.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/q9m59lK28yO4VWh3q4V30o86rUa.jpg",
        "video_url": "https://www.youtube.com/watch?v=VFsMuDlimuA",
        "rating": 8.6,
        "release_year": 2016,
        "language": "English",
        "duration": "2h 14m",
        "cast": "Vera Farmiga, Patrick Wilson, Frances O'Connor",
        "crew": "Director: James Wan",
        "parent": conjuring_parent,
        "part_number": 2,
        "part_name": "The Conjuring 2"
    },
    genre_slugs=['horror', 'thriller']
)

upsert_movie(
    title="The Conjuring: The Devil Made Me Do It",
    defaults={
        "description": "A chilling story of terror, murder and unknown evil that shocked even experienced real-life paranormal investigators Ed and Lorraine Warren.",
        "content_type": "movie",
        "poster_url": "https://image.tmdb.org/t/p/original/xbSu194Lh1VvG25v5a7t67v9C1k.jpg",
        "banner_url": "https://image.tmdb.org/t/p/original/qi6v4x7jG7XnPEU4r792345O.jpg",
        "video_url": "https://www.youtube.com/watch?v=h9Q4zZsOPTU",
        "rating": 8.2,
        "release_year": 2021,
        "language": "English",
        "duration": "1h 52m",
        "cast": "Vera Farmiga, Patrick Wilson, Ruairi O'Connor",
        "crew": "Director: Michael Chaves",
        "parent": conjuring_parent,
        "part_number": 3,
        "part_name": "The Devil Made Me Do It"
    },
    genre_slugs=['horror', 'thriller']
)

# 6. TV Show Seasons: Stranger Things
try:
    st_parent = Movie.objects.get(title="Stranger Things")
    st_parent.duration = "5 Seasons"
    st_parent.video_url = "https://www.youtube.com/watch?v=yQEondeGvKo"
    st_parent.save()
    
    for s_num in range(1, 6):
        s_yt_urls = {
            1: "https://www.youtube.com/watch?v=b9EkMc79ZSU",
            2: "https://www.youtube.com/watch?v=vgS2L7WPIO4",
            3: "https://www.youtube.com/watch?v=YEG3bmU_WaI",
            4: "https://www.youtube.com/watch?v=yQEondeGvKo",
            5: "https://www.youtube.com/watch?v=b1BvO8Zp3wY"
        }
        s_desc = {
            1: "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
            2: "It's 1984 and the citizens of Hawkins, Indiana are still reeling from the horrors of the Demogorgon and the secrets of Hawkins Lab. Will Byers has been rescued from the Upside Down but a bigger, sinister entity still threatens those who survived.",
            3: "Budding romance, a new mall, and a menacing threat looming in the summer heat of 1985 in Hawkins. Old and new enemies are reminding everyone that evil never ends; it explains and evolves.",
            4: "It's been six months since the Battle of Starcourt, which brought terror and destruction to Hawkins. Struggling with the aftermath, our group of friends are separated for the first time.",
            5: "The final season of the epic saga, as the gang confronts the Upside Down once and for all."
        }
        upsert_movie(
            title=f"Stranger Things: Season {s_num}",
            defaults={
                "description": s_desc[s_num],
                "content_type": "series",
                "poster_url": "https://image.tmdb.org/t/p/original/uOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                "video_url": s_yt_urls[s_num],
                "rating": 9.2 if s_num in [1, 5] else (9.0 if s_num == 2 else (8.9 if s_num == 3 else 9.3)),
                "release_year": 2015 + s_num if s_num < 4 else (2022 if s_num == 4 else 2025),
                "language": "English",
                "duration": "8 Episodes" if s_num in [1, 3, 5] else "9 Episodes",
                "cast": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour",
                "crew": "Creators: The Duffer Brothers",
                "parent": st_parent,
                "part_number": s_num,
                "part_name": f"Season {s_num}"
            },
            genre_slugs=['horror', 'sci-fi', 'thriller']
        )
except Movie.DoesNotExist:
    pass

print("Idempotent seeding completed successfully!")
