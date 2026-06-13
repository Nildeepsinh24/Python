from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cine_verse.models import Genre, Movie, UserProfile, WatchHistory
import urllib.request
import urllib.error
import urllib.parse
import ssl

class Command(BaseCommand):
    help = 'Seeds database with high-quality CineVerse OTT real movie and series data'

    def handle(self, *args, **kwargs):
        youtube_trailers = {
            'Interstellar': 'https://www.youtube.com/watch?v=zSWdZAIB5nY',
            'Dune: Part Two': 'https://www.youtube.com/watch?v=Way9Dexny3w',
            'The Dark Knight': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
            'Inception': 'https://www.youtube.com/watch?v=YoHD9XEInc0',
            'Oppenheimer': 'https://www.youtube.com/watch?v=uYPbbEsJkQ0',
            'Gladiator': 'https://www.youtube.com/watch?v=P5ieIbInFpg',
            'Mad Max: Fury Road': 'https://www.youtube.com/watch?v=hEJnMQG9ev8',
            'John Wick: Chapter 4': 'https://www.youtube.com/watch?v=qEVUqWsJtJA',
            'The Godfather': 'https://www.youtube.com/watch?v=UaVTIH8mujA',
            'The Shawshank Redemption': 'https://www.youtube.com/watch?v=PLl99DlL6b4',
            'Parasite': 'https://www.youtube.com/watch?v=5xH0HfJHsaY',
            'Get Out': 'https://www.youtube.com/watch?v=sRfnevzM9J8',
            'The Conjuring': 'https://www.youtube.com/watch?v=k10ETZ42q5o',
            'Hereditary': 'https://www.youtube.com/watch?v=V6wWKNij_1M',
            'A Quiet Place': 'https://www.youtube.com/watch?v=WR7cc5t7tv8',
            'Avatar: The Way of Water': 'https://www.youtube.com/watch?v=d9MyW72ELq0',
            'Blade Runner 2049': 'https://www.youtube.com/watch?v=gCcx85zbxz4',
            'Spider-Man: No Way Home': 'https://www.youtube.com/watch?v=JfVOs4VSpmA',
            'Shutter Island': 'https://www.youtube.com/watch?v=5iaYLCip5Qk',
            'The Hangover': 'https://www.youtube.com/watch?v=tcdUhdOlz9M',
            'Superbad': 'https://www.youtube.com/watch?v=N_ASi32tue8',
            'It': 'https://www.youtube.com/watch?v=FnCdOQs95i8',
            'The Matrix': 'https://www.youtube.com/watch?v=vKQi3bBA1y8',
            'Spirited Away': 'https://www.youtube.com/watch?v=ByXuk9QqQkk',
            'Spider-Man: Across the Spider-Verse': 'https://www.youtube.com/watch?v=cqGjhVJWtEg',
            'Avengers: Endgame': 'https://www.youtube.com/watch?v=TcMBFSGVi1c',
            'The Lord of the Rings: The Fellowship of the Ring': 'https://www.youtube.com/watch?v=V75dMMIW2B4',
            'The Shining': 'https://www.youtube.com/watch?v=KI19-sS57LI',
            'A Nightmare on Elm Street': 'https://www.youtube.com/watch?v=dCVh4lBfW-c',
            'Talk to Me': 'https://www.youtube.com/watch?v=aLAKJu9aUXo',
            'M3GAN': 'https://www.youtube.com/watch?v=WrR7cc5t7tv8',
            'Project Hail Mary': 'https://www.youtube.com/watch?v=zSWdZAIB5nY',
            'Stranger Things': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'The Boys': 'https://www.youtube.com/watch?v=M1BHuPScwbg',
            'Shōgun': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'Breaking Bad': 'https://www.youtube.com/watch?v=HhesaQXLuRY',
            'Succession': 'https://www.youtube.com/watch?v=OzY2qqZpe2A',
            'The Office': 'https://www.youtube.com/watch?v=LHOtME2DLyI',
            'Friends': 'https://www.youtube.com/watch?v=hDNNmeeJs1Q',
            'Ted Lasso': 'https://www.youtube.com/watch?v=3m_R-1t-hEE',
            'The Legend of Vox Machina': 'https://www.youtube.com/watch?v=JvxBy_3PsnU',
            'Wednesday': 'https://www.youtube.com/watch?v=Di310WS8zLk',
            'The Night Manager': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'From': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'Alice in the Borderland': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'Moon Knight': 'https://www.youtube.com/watch?v=x7Krla_UxHg',
            'Dark': 'https://www.youtube.com/watch?v=rrwyCJ08qFM',
            'Chernobyl': 'https://www.youtube.com/watch?v=s9APLXM9Ei8',
            'The Boroughs': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'Spider-Noir': 'https://www.youtube.com/watch?v=yQEondeGvKo',
            'Scam 1992: The Harshad Mehta Story': 'https://www.youtube.com/watch?v=XXsnsk6S6Qk',
            'Farzi': 'https://www.youtube.com/watch?v=33-J_V_t56A',
            'The Family Man': 'https://www.youtube.com/watch?v=bv9xrcqcMys',
            'Asur: Welcome to Your Dark Side': 'https://www.youtube.com/watch?v=9AZnfGUnPZB',
        }
        self.stdout.write("Deleting existing data...")
        WatchHistory.objects.all().delete()
        Movie.objects.all().delete()
        Genre.objects.all().delete()
        
        self.stdout.write("Creating genres...")
        genres_data = [
            {'name': 'Action', 'slug': 'action'},
            {'name': 'Sci-Fi', 'slug': 'sci-fi'},
            {'name': 'Drama', 'slug': 'drama'},
            {'name': 'Thriller', 'slug': 'thriller'},
            {'name': 'Comedy', 'slug': 'comedy'},
            {'name': 'Horror', 'slug': 'horror'},
            {'name': 'Adventure', 'slug': 'adventure'},
            {'name': 'Crime', 'slug': 'crime'},
            {'name': 'Mystery', 'slug': 'mystery'},
            {'name': 'Biography', 'slug': 'biography'},
        ]
        
        genres_map = {}
        for g in genres_data:
            genre, created = Genre.objects.get_or_create(slug=g['slug'], defaults={'name': g['name']})
            genres_map[g['slug']] = genre

        poster_overrides = {
            'Interstellar': 'https://image.tmdb.org/t/p/original/gEU2v4vSCNW3xtm24TIcl7u4n5D.jpg',
            'Dune: Part Two': 'https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            'The Dark Knight': 'https://rukminim2.flixcart.com/image/480/640/xif0q/poster/i/i/b/medium-dark-knight-rises-batman-fire-logo-background-wall-poster-original-imagqfyqmsdjmahp.jpeg?q=90',
            'Inception': 'https://wallpapercat.com/w/full/9/6/1/304867-1536x2732-iphone-hd-inception-background-image.jpg',
            'Oppenheimer': 'https://m.media-amazon.com/images/I/51TdQ4sompL.jpg',
            'Gladiator': 'https://image.tmdb.org/t/p/original/ty8hDCccv7Jzzq3t5ikLExRqySg.jpg',
            'Mad Max: Fury Road': 'https://movieposterhub.com/cdn/shop/files/MADMADFURYROAD-MAX.jpg?crop=center&height=1200&v=1706768763&width=1200',
            'John Wick: Chapter 4': 'https://image.tmdb.org/t/p/original/vZ02e421JxsoRWaIIAqVI2KE.jpg',
            'The Godfather': 'https://wallpapercave.com/wp/wp12115434.jpg',
            'The Shawshank Redemption': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRD1VWS5ADAVUQZbSi0trMPSZfIwOLZ2VYPSw&s',
            'Parasite': 'https://images.wallpapersden.com/image/download/parasite-movie-poster_a25la2eUmZqaraWkpJRmbmdlrWZlbWU.jpg',
            'Get Out': 'https://m.media-amazon.com/images/M/MV5BOGMzMjFiMDUtZWQ5Ny00MTUyLWEyYzItMzcwNzJjNzBmMjI4XkEyXkFqcGc@._V1_.jpg',
            'The Conjuring': 'https://images.static-bluray.com/movies/uvcovers/3274_large.jpg',
            'Hereditary': 'https://images2.alphacoders.com/112/1122556.jpg',
            'A Quiet Place': 'https://lh5.googleusercontent.com/proxy/NUylUXnFwN2gzEqgzJpQAuM7DQGp0BH6f-HDFNao8O-2g0KrZjBJ6D-KiOG7L-j3ftkawdxHZZfdkQu9XeFEHnd0LnnPJnIHVOqE-Z8XSVDgHw',
            'Avatar: The Way of Water': 'https://cdn.district.in/movies-assets/images/cinema/avatar-7024be30-a01c-11f0-8de5-1d5c271d84c8.jpg?im=Resize,width=720',
            'Blade Runner 2049': 'https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_FMjpg_UX1000_.jpg',
            'Shutter Island': 'https://w0.peakpx.com/wallpaper/98/690/HD-wallpaper-shutter-island-screen-printed-movie-poster.jpg',
            'The Hangover': 'https://image.tmdb.org/t/p/original/wzLMIElewg7XFATaaODnncoe6Td.jpg',
            'Superbad': 'https://www.acmodasi.in/amdb/images/movie/z/k/superbad-2007-39916.jpg',
            'It': 'https://i.ebayimg.com/00/s/MTYwMFgxMDg2/z/qHwAAOSw1Y5dcuMC/$_57.JPG?set_id=8800005007',
            'The Matrix': 'https://c4.wallpaperflare.com/wallpaper/614/687/784/movies-matrix-movie-poster-poster-the-matrix-resurrections-hd-wallpaper-preview.jpg',
            'Spirited Away': 'https://c4.wallpaperflare.com/wallpaper/920/355/589/cihiro-disney-spirited-away-entertainment-movies-hd-art-wallpaper-preview.jpg',
            'Spider-Man: Across the Spider-Verse': 'https://preview.redd.it/official-poster-for-spider-man-across-the-spider-verse-v0-yogt3cuj727a1.jpg?width=640&crop=smart&auto=webp&s=b5d25d425beaae300ed10c7237e015816e0fe01b',
            'Avengers: Endgame': 'https://m.media-amazon.com/images/I/713yG1FcfhL._AC_UF894,1000_QL80_.jpg',
            'The Lord of the Rings: The Fellowship of the Ring': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEaOTjjsH93_nbzlb8EI124CNG6wq4UUTfhA&s',
            'The Shining': 'https://beaumonteventstx.com/wp-content/uploads/2024/08/HD-wallpaper-movie-the-shining.jpg',
            'A Nightmare on Elm Street': 'https://c4.wallpaperflare.com/wallpaper/307/220/1/2010-a-nightmare-on-elm-street-movie-wallpaper-preview.jpg',
            'Talk to Me': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWlBOR2EuEO3Cod7-rQumorBDOKX91wf1_VQ&s',
            'M3GAN': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgL6_djuzpvG6Hl4LDMfSOCRNgPsbqONAQ_Q&s',
            'Project Hail Mary': 'https://media.themoviedb.org/t/p/w220_and_h330_face/mSevmySMoq6E5JZVrLXACUUo0n5.jpg',
            'Spider-Man: No Way Home': 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618',
            'From': 'https://image.tmdb.org/t/p/original/uV65yaFkw6B4KHXAsBYui0KvJq.jpg',
            'Alice in the Borderland': 'https://m.media-amazon.com/images/I/61BusO1K0hL._AC_UF894,1000_QL80_.jpg',
            'Moon Knight': 'https://m.media-amazon.com/images/M/MV5BNDAzNmYwZjgtNDc3YS00ZDMyLTk0MjktMTg4MGNmNGU3MjlhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            'Breaking Bad': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQeyQJOmXbTuKCFsSwBdtE6vCHJa1Up25JuQ&s',
            'Succession': 'https://w0.peakpx.com/wallpaper/436/68/HD-wallpaper-tv-show-succession.jpg',
            'The Office': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7GWdvxZk119nQPj-kjlm7Z_fyC3aO3QMyWg&s',
            'Friends': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAgxBT98RVJZzj7xJrGI_DC1pVh7VmvF3UuQ&s',
            'Ted Lasso': 'https://lh4.googleusercontent.com/proxy/0KyQhkSlogOqldlFAMeu9xrUyJ2kfb6jLRwAnnhrbIXQgidiWbSK1NuD7Egl7ZfKN6wrSEQXMr0rHjBAxT51uP92Lpc',
            'The Legend of Vox Machina': 'https://images.wallpapersden.com/image/download/the-legend-of-vox-machina-season-2_bmVua2aUmZqaraWkpJRobWllrWdma2U.jpg',
            'Wednesday': 'https://images.wallpapersden.com/image/download/netflix-wednesday-2022_bW1mbm2UmZqaraWkpJRmbmdlrWZlbWU.jpg',
        }
            
        self.stdout.write("Creating movies & series...")
        created_movies = []

        real_media = [
            # Movies
            {
                "title": "Interstellar",
                "description": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
                "poster_url": "https://image.tmdb.org/t/p/original/gEU2v4vSCNW3xtm24TIcl7u4n5D.jpg",
                "banner_url": "https://wallpaperaccess.com/full/300686.jpg",
                "rating": 9.8,
                "release_year": 2014,
                "language": "English",
                "duration": "2h 49m",
                "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine",
                "crew": "Director: Christopher Nolan",
                "display_order": 10,
                "genres": ["sci-fi", "drama", "adventure"],
                "is_trending": True, "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Dune: Part Two",
                "description": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family.",
                "poster_url": "https://image.tmdb.org/t/p/original/czemboc07Bhv5822LqyqtEDZ582.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
                "rating": 9.6,
                "release_year": 2024,
                "language": "English",
                "duration": "2h 46m",
                "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem",
                "crew": "Director: Denis Villeneuve",
                "display_order": 20,
                "genres": ["sci-fi", "adventure", "action"],
                "is_trending": True, "is_popular": True, "is_latest": True
            },
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "poster_url": "https://rukminim2.flixcart.com/image/480/640/xif0q/poster/i/i/b/medium-dark-knight-rises-batman-fire-logo-background-wall-poster-original-imagqfyqmsdjmahp.jpeg?q=90",
                "banner_url": "https://image.tmdb.org/t/p/original/cfT29Im5VDvjE0RpyKOSdCKZal7.jpg",
                "rating": 9.7,
                "release_year": 2008,
                "language": "English",
                "duration": "2h 32m",
                "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Maggie Gyllenhaal",
                "crew": "Director: Christopher Nolan",
                "display_order": 30,
                "genres": ["action", "drama", "thriller"],
                "is_trending": True, "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "poster_url": "https://image.tmdb.org/t/p/original/lpmUu3xkoksz3xsa1feIUoOBZrg.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/8ZTVqvKDQ8emSGUEMjsS4yHAwrp.jpg",
                "rating": 9.4,
                "release_year": 2010,
                "language": "English",
                "duration": "2h 28m",
                "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
                "crew": "Director: Christopher Nolan",
                "display_order": 40,
                "genres": ["action", "sci-fi", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Oppenheimer",
                "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
                "poster_url": "https://image.tmdb.org/t/p/original/fm6IpvlNyccu5xU028n7TAU9xq7.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/neeNHeXjMF5fXoCJRsOmkNGC7q.jpg",
                "rating": 9.3,
                "release_year": 2023,
                "language": "English",
                "duration": "3h 00m",
                "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.",
                "crew": "Director: Christopher Nolan",
                "display_order": 50,
                "genres": ["drama", "thriller"],
                "is_trending": True, "is_popular": True, "is_latest": True
            },
            {
                "title": "Gladiator",
                "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
                "poster_url": "https://image.tmdb.org/t/p/original/ty8hDCccv7Jzzq3t5ikLExRqySg.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/jhk6D8pim3yaByu1801kMoxXFaX.jpg",
                "rating": 9.1,
                "release_year": 2000,
                "language": "English",
                "duration": "2h 35m",
                "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed",
                "crew": "Director: Ridley Scott",
                "display_order": 60,
                "genres": ["action", "drama", "adventure"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Mad Max: Fury Road",
                "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.",
                "poster_url": "https://image.tmdb.org/t/p/original/h1B7t5iklEp3bufwDq4n9jTRSwY.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/uT895WNwm0aIJRtGizcQhrejWUo.jpg",
                "rating": 9.0,
                "release_year": 2015,
                "language": "English",
                "duration": "2h 00m",
                "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult, Zoë Kravitz",
                "crew": "Director: George Miller",
                "display_order": 70,
                "genres": ["action", "adventure", "sci-fi"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "John Wick: Chapter 4",
                "description": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe.",
                "poster_url": "https://image.tmdb.org/t/p/original/vZ02e421JxsoRWaIIAqVI2KE.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg",
                "rating": 8.9,
                "release_year": 2023,
                "language": "English",
                "duration": "2h 49m",
                "cast": "Keanu Reeves, Donnie Yen, Bill Skarsgård, Laurence Fishburne",
                "crew": "Director: Chad Stahelski",
                "display_order": 80,
                "genres": ["action", "thriller"],
                "is_trending": True, "is_latest": True
            },
            {
                "title": "The Godfather",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "poster_url": "https://image.tmdb.org/t/p/original/3bhDafwDq4n9jTRSwYvOwunzW4dx.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/tSPT36ZKlP2WVHJLM4cQPLSzv3b.jpg",
                "rating": 9.9,
                "release_year": 1972,
                "language": "English",
                "duration": "2h 55m",
                "cast": "Marlon Brando, Al Pacino, James Caan, Diane Keaton",
                "crew": "Director: Francis Ford Coppola",
                "display_order": 90,
                "genres": ["drama", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "The Shawshank Redemption",
                "description": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
                "poster_url": "https://image.tmdb.org/t/p/original/q6v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/zfbjgQE1uSd9wiPTX4VzsLi0rGG.jpg",
                "rating": 9.9,
                "release_year": 1994,
                "language": "English",
                "duration": "2h 22m",
                "cast": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
                "crew": "Director: Frank Darabont",
                "display_order": 100,
                "genres": ["drama"],
                "is_trending": True, "is_top_rated": True
            },
            {
                "title": "Parasite",
                "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                "poster_url": "https://image.tmdb.org/t/p/original/7ii41pzulFnu64FmsoFSesCmbVg.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
                "rating": 9.3,
                "release_year": 2019,
                "language": "Korean",
                "duration": "2h 12m",
                "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik",
                "crew": "Director: Bong Joon Ho",
                "display_order": 110,
                "genres": ["drama", "thriller", "comedy"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Get Out",
                "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception eventually reaches a boiling point.",
                "poster_url": "https://image.tmdb.org/t/p/original/1swX7y3kfTYwfHqo37Uj9foNnZW.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/o8dPH0ZSIyyViP6rjRX1djwCUwI.jpg",
                "rating": 8.7,
                "release_year": 2017,
                "language": "English",
                "duration": "1h 44m",
                "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford, Catherine Keener",
                "crew": "Director: Jordan Peele",
                "display_order": 120,
                "genres": ["horror", "thriller"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "The Conjuring",
                "description": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
                "poster_url": "https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg",
                "rating": 8.5,
                "release_year": 2013,
                "language": "English",
                "duration": "1h 52m",
                "cast": "Vera Farmiga, Patrick Wilson, Lili Taylor, Ron Livingston",
                "crew": "Director: James Wan",
                "display_order": 130,
                "genres": ["horror", "thriller"],
                "is_popular": True
            },
            {
                "title": "Hereditary",
                "description": "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother.",
                "poster_url": "https://image.tmdb.org/t/p/original/44nzrIin2PQxOhgqnS4S4JNiAmQ.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/gJbTXKNTL6O7r7PzF6ZRkJGBlPp.jpg",
                "rating": 8.4,
                "release_year": 2018,
                "language": "English",
                "duration": "2h 07m",
                "cast": "Toni Collette, Milly Shapiro, Alex Wolff, Gabriel Byrne",
                "crew": "Director: Ari Aster",
                "display_order": 140,
                "genres": ["horror", "drama"],
                "is_trending": True
            },
            {
                "title": "A Quiet Place",
                "description": "A family must navigate their lives in silence to avoid mysterious creatures that hunt by sound.",
                "poster_url": "https://image.tmdb.org/t/p/original/nmgOd3X2Xn3jIp9OLCRJzLExRWN.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/nHRUtBwFNnNN70vcQ7lAsjc2T6S.jpg",
                "rating": 8.8,
                "release_year": 2018,
                "language": "English",
                "duration": "1h 30m",
                "cast": "Emily Blunt, John Krasinski, Millicent Simmonds, Noah Jupe",
                "crew": "Director: John Krasinski",
                "display_order": 150,
                "genres": ["horror", "sci-fi", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Avatar: The Way of Water",
                "description": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
                "poster_url": "https://image.tmdb.org/t/p/original/uXTg565ahu9RwonCX1V2Hex1NU6.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/qnzQm0PCVnSyv1dqpVmRgMWHbLD.jpg",
                "rating": 8.7,
                "release_year": 2022,
                "language": "English",
                "duration": "3h 12m",
                "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver, Kate Winslet",
                "crew": "Director: James Cameron",
                "display_order": 160,
                "genres": ["sci-fi", "adventure", "action"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "Blade Runner 2049",
                "description": "A new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos.",
                "poster_url": "https://image.tmdb.org/t/p/original/gajK78XbsxiKKnTOAOnVSzGZEAe.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/mVr0UiqyltcfqxbAUcLl9zWL8ah.jpg",
                "rating": 8.9,
                "release_year": 2017,
                "language": "English",
                "duration": "2h 44m",
                "cast": "Ryan Gosling, Harrison Ford, Ana de Armas, Sylvia Hoeks",
                "crew": "Director: Denis Villeneuve",
                "display_order": 170,
                "genres": ["sci-fi", "thriller", "drama"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "Spider-Man: No Way Home",
                "description": "Peter Parker's life and reputation are upended when a spell gone wrong opens the multiverse and brings dangerous visitors into his world.",
                "poster_url": "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618",
                "banner_url": "https://image.tmdb.org/t/p/original/tyQo080tijexyUHBvWPwQt26bZa.jpg",
                "rating": 9.1,
                "release_year": 2021,
                "language": "English",
                "duration": "2h 28m",
                "cast": "Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon",
                "crew": "Director: Jon Watts",
                "display_order": 180,
                "genres": ["action", "adventure", "sci-fi"],
                "is_trending": True, "is_popular": True, "is_latest": True
            },
            {
                "title": "Shutter Island",
                "description": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.",
                "poster_url": "https://image.tmdb.org/t/p/original/49oxrx541p02ew2ew1xxy5hedhk.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/rbZvGN1A1QyZuoKzhCw8QPmf2q0.jpg",
                "rating": 9.0,
                "release_year": 2010,
                "language": "English",
                "duration": "2h 18m",
                "cast": "Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley, Michelle Williams",
                "crew": "Director: Martin Scorsese",
                "display_order": 190,
                "genres": ["thriller", "drama"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "The Hangover",
                "description": "Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night and the bachelor missing.",
                "poster_url": "https://image.tmdb.org/t/p/original/9MsrtT34QUUBhhmU0YEZ8TJwDfH.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/iuRVt8tFiXDPGgzavhuSa3QHRxD.jpg",
                "rating": 8.2,
                "release_year": 2009,
                "language": "English",
                "duration": "1h 40m",
                "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis, Justin Bartha",
                "crew": "Director: Todd Phillips",
                "display_order": 200,
                "genres": ["comedy"],
                "is_popular": True
            },
            {
                "title": "Superbad",
                "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-fueled party goes awry.",
                "poster_url": "https://image.tmdb.org/t/p/original/Ak46cQFDOXWmuU11bzyWUmN8Ebg.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/coru98UcFBzJIU7bxZguxaePgu0.jpg",
                "rating": 8.3,
                "release_year": 2007,
                "language": "English",
                "duration": "1h 53m",
                "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse, Bill Hader",
                "crew": "Director: Greg Mottola",
                "display_order": 210,
                "genres": ["comedy"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "It",
                "description": "In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of their town.",
                "poster_url": "https://image.tmdb.org/t/p/original/yYG7Rhn9HfFpssIMeNiDynvxC14.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/qVGpxnjrGlHaSTCqTQI6viBDSfp.jpg",
                "rating": 8.4,
                "release_year": 2017,
                "language": "English",
                "duration": "2h 15m",
                "cast": "Bill Skarsgård, Jaeden Martell, Finn Wolfhard, Sophia Lillis",
                "crew": "Director: Andy Muschietti",
                "display_order": 220,
                "genres": ["horror", "thriller"],
                "is_popular": True
            },
            {
                "title": "The Matrix",
                "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
                "poster_url": "https://image.tmdb.org/t/p/original/f89QPU_K57LY2IQ4f4E5n4slweZ.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/tlm8UkiQsitc8rSuIAscQDCnP8d.jpg",
                "rating": 9.5,
                "release_year": 1999,
                "language": "English",
                "duration": "2h 16m",
                "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
                "crew": "Director: The Wachowskis",
                "display_order": 230,
                "genres": ["sci-fi", "action"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Spirited Away",
                "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
                "poster_url": "https://image.tmdb.org/t/p/original/3oRndZT_BC7cp-RVMbKX4enRonx.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/dyJvKsNs2KP8qQnAXbRwDjblViy.jpg",
                "rating": 9.6,
                "release_year": 2001,
                "language": "Japanese",
                "duration": "2h 05m",
                "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
                "crew": "Director: Hayao Miyazaki",
                "display_order": 240,
                "genres": ["adventure", "drama"],
                "is_trending": True, "is_top_rated": True
            },
            {
                "title": "Spider-Man: Across the Spider-Verse",
                "description": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence. When the heroes clash on how to handle a new threat, Miles must redefine what it means to be a hero.",
                "poster_url": "https://image.tmdb.org/t/p/original/8Gxv2Z72j5t2hj2wReVqYiM9a.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/9xfDWXAUbFXQK585JvByT5pEAhe.jpg",
                "rating": 9.5,
                "release_year": 2023,
                "language": "English",
                "duration": "2h 20m",
                "cast": "Shameik Moore, Hailee Steinfeld, Oscar Isaac, Jake Johnson",
                "crew": "Directors: Joaquim Dos Santos, Kemp Powers",
                "display_order": 250,
                "genres": ["action", "adventure", "sci-fi"],
                "is_trending": True, "is_popular": True, "is_latest": True
            },
            {
                "title": "Avengers: Endgame",
                "description": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
                "poster_url": "https://image.tmdb.org/t/p/original/or7PzF6ZRkJGBlPp6oom5QYQ2yQ.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
                "rating": 9.2,
                "release_year": 2019,
                "language": "English",
                "duration": "3h 01m",
                "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
                "crew": "Directors: Anthony Russo, Joe Russo",
                "display_order": 260,
                "genres": ["action", "sci-fi", "adventure"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
                "poster_url": "https://image.tmdb.org/t/p/original/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/oiwc338EoBgS4sEI2ixAny4KQKg.jpg",
                "rating": 9.8,
                "release_year": 2001,
                "language": "English",
                "duration": "2h 58m",
                "cast": "Elijah Wood, Ian McKellen, Orlando Bloom, Viggo Mortensen",
                "crew": "Director: Peter Jackson",
                "display_order": 270,
                "genres": ["adventure", "action", "drama"],
                "is_trending": True, "is_popular": True, "is_top_rated": True
            },
            {
                "title": "The Shining",
                "description": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future.",
                "poster_url": "https://image.tmdb.org/t/p/original/m7WyGJRiOq88PFw7es7nAYz2Cxj.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/mmd1HnuvAzFc4iuVJcnBrhDNEKr.jpg",
                "rating": 9.0,
                "release_year": 1980,
                "language": "English",
                "duration": "2h 26m",
                "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd, Scatman Crothers",
                "crew": "Director: Stanley Kubrick",
                "display_order": 280,
                "genres": ["horror", "drama"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "A Nightmare on Elm Street",
                "description": "The monstrous spirit of a slain child murderer seeks revenge by invading the dreams of teenagers whose parents were responsible for his untimely demise.",
                "poster_url": "https://image.tmdb.org/t/p/original/pE8X788agG0zQujud44hTj0ZAWz.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/nzSjTiecdosBfwMGAdpt9CxltCI.jpg",
                "rating": 8.1,
                "release_year": 1984,
                "language": "English",
                "duration": "1h 31m",
                "cast": "Heather Langenkamp, Johnny Depp, Robert Englund",
                "crew": "Director: Wes Craven",
                "display_order": 290,
                "genres": ["horror", "thriller"],
                "is_trending": True
            },
            {
                "title": "Talk to Me",
                "description": "When a group of friends discover how to conjure spirits using an embalmed hand, they become hooked on the new thrill, until one of them goes too far and unleashes terrifying supernatural forces.",
                "poster_url": "https://image.tmdb.org/t/p/original/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/46Os8U0DEPmI0OnvKDxucl6SLVZ.jpg",
                "rating": 8.3,
                "release_year": 2023,
                "language": "English",
                "duration": "1h 35m",
                "cast": "Sophie Wilde, Alexandra Jensen, Joe Bird",
                "crew": "Directors: Danny Philippou, Michael Philippou",
                "display_order": 300,
                "genres": ["horror", "thriller"],
                "is_trending": True, "is_latest": True
            },
            {
                "title": "M3GAN",
                "description": "A toy-company roboticist builds a life-like doll that begins to take on a life of its own, leading to terrifying consequences.",
                "poster_url": "https://image.tmdb.org/t/p/original/stTEyZ3y8kPrP927jZ922R4lY3k.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/qd4EKTuudkws9lW76Dn9C0tnuVA.jpg",
                "rating": 8.0,
                "release_year": 2022,
                "language": "English",
                "duration": "1h 42m",
                "cast": "Allison Williams, Violet McGraw, Ronny Chieng",
                "crew": "Director: Gerard Johnstone",
                "display_order": 310,
                "genres": ["horror", "sci-fi"],
                "is_popular": True
            },
            {
                "title": "Project Hail Mary",
                "description": "A lone astronaut embarks on a desperate, last-chance mission to save humanity, discovering unexpected allies and relying on ingenuity to survive.",
                "poster_url": "https://image.tmdb.org/t/p/original/placeholder_project_hail_mary.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/yihdXomYb5kTeSivtFndMy5iDmf.jpg",
                "rating": 8.5,
                "release_year": 2024,
                "language": "English",
                "duration": "2h 30m",
                "cast": "Ryan Gosling, Emily Blunt",
                "crew": "Director: Phil Lord, Christopher Miller",
                "display_order": 320,
                "genres": ["sci-fi", "drama", "adventure"],
                "is_popular": True, "is_latest": True
            },
            
            # TV Series
            {
                "title": "Stranger Things",
                "description": "Currently trending on Netflix. When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
                "poster_url": "https://image.tmdb.org/t/p/original/uOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                "rating": 9.6,
                "release_year": 2025,
                "language": "English",
                "duration": "TV Series",
                "cast": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour",
                "crew": "Creators: The Duffer Brothers",
                "display_order": 330,
                "genres": ["horror", "sci-fi", "thriller"],
                "is_trending": True, "is_popular": True, "is_latest": True, "is_top_rated": True
            },
            {
                "title": "The Boys",
                "description": "Currently trending on Prime Video. A fun, gritty, and dark superhero series focusing on a group of vigilantes set out to take down corrupt superheroes who abuse their superpowers.",
                "poster_url": "https://image.tmdb.org/t/p/original/in1R2dDc421JxsoRWaIIAqVI2KE.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/bq28ajZaoMyzEIm6REelqyqtEDZ.jpg",
                "rating": 9.4,
                "release_year": 2024,
                "language": "English",
                "duration": "TV Series",
                "cast": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty",
                "crew": "Creator: Eric Kripke",
                "display_order": 340,
                "genres": ["action", "sci-fi", "comedy"],
                "is_trending": True, "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Shōgun",
                "description": "Currently trending on Disney+ Hotstar. In Japan in the year 1600, Lord Yoshii Toranaga struggles for his life as his enemies on the Council of Regents unite against him.",
                "poster_url": "https://image.tmdb.org/t/p/original/knnGreFnQqhufzg9AqjzeMD7k5I.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/6Tb87q9Tog30F5AAHh1gyDT2Vve.jpg",
                "rating": 9.5,
                "release_year": 2024,
                "language": "Japanese",
                "duration": "TV Series",
                "cast": "Hiroyuki Sanada, Cosmo Jarvis, Anna Sawai",
                "crew": "Creators: Rachel Kondo, Justin Marks",
                "display_order": 350,
                "genres": ["drama", "action"],
                "is_trending": True, "is_popular": True, "is_latest": True, "is_top_rated": True
            },
            {
                "title": "Breaking Bad",
                "description": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student in order to secure his family's future.",
                "poster_url": "https://image.tmdb.org/t/p/original/ztkK60SrqWp2XMkBfLgdBhx5EJ82.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg",
                "rating": 9.9,
                "release_year": 2008,
                "language": "English",
                "duration": "TV Series",
                "cast": "Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk",
                "crew": "Creator: Vince Gilligan",
                "display_order": 360,
                "genres": ["drama", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Succession",
                "description": "The Roy family is known for controlling the biggest media and entertainment company in the world. However, their world changes when their father steps down from the company.",
                "poster_url": "https://image.tmdb.org/t/p/original/74uVSgg0te6TVHnUqbJ6GVzIx1r.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/bcdUYUFk8GdpZJPiSAas9UeocLH.jpg",
                "rating": 9.4,
                "release_year": 2018,
                "language": "English",
                "duration": "TV Series",
                "cast": "Brian Cox, Jeremy Strong, Sarah Snook, Kieran Culkin",
                "crew": "Creator: Jesse Armstrong",
                "display_order": 370,
                "genres": ["drama", "comedy"],
                "is_trending": True, "is_popular": True, "is_top_rated": True
            },
            {
                "title": "The Office",
                "description": "A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.",
                "poster_url": "https://image.tmdb.org/t/p/original/37Uj9foNnZWhgdYS_EcN2Ix8mzi.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/mLyW3UTgi2lsMdtueYODcfAB9Ku.jpg",
                "rating": 9.2,
                "release_year": 2005,
                "language": "English",
                "duration": "TV Series",
                "cast": "Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer",
                "crew": "Developer: Greg Daniels",
                "display_order": 380,
                "genres": ["comedy"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Friends",
                "description": "Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.",
                "poster_url": "https://image.tmdb.org/t/p/original/f4FFv3wM5uf6RANFKmIHg7LK6de.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/m3Jev59mJLyUp5bXhY5SVfIBZI0.jpg",
                "rating": 9.0,
                "release_year": 1994,
                "language": "English",
                "duration": "TV Series",
                "cast": "Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry, David Schwimmer",
                "crew": "Creators: David Crane, Marta Kauffman",
                "display_order": 390,
                "genres": ["comedy"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Ted Lasso",
                "description": "American college football coach Ted Lasso heads to London to manage a struggling English Premier League football team, AFC Richmond.",
                "poster_url": "https://image.tmdb.org/t/p/original/2z142q40vjhFO0DrUwp0kYBZaPH.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/gEQkOMmnJcoh9Hh1vk7fpVYnksR.jpg",
                "rating": 9.1,
                "release_year": 2020,
                "language": "English",
                "duration": "TV Series",
                "cast": "Jason Sudeikis, Hannah Waddingham, Jeremy Swift, Phil Dunster",
                "crew": "Creators: Jason Sudeikis, Bill Lawrence",
                "display_order": 400,
                "genres": ["comedy", "drama"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "The Legend of Vox Machina",
                "description": "They're rowdy, they're ragtag, they're misfits turned mercenaries for hire. Vox Machina is more interested in easy money and cheap ale than actually protecting the realm.",
                "poster_url": "https://image.tmdb.org/t/p/original/vOwunzW4dx3n0J5mH40n9jTRSwY.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/qCGwPCwlSiLdlYinzy9rSQDjQX1.jpg",
                "rating": 8.9,
                "release_year": 2022,
                "language": "English",
                "duration": "TV Series",
                "cast": "Laura Bailey, Ashley Johnson, Matthew Mercer, Liam O'Brien",
                "crew": "Creators: Critical Role",
                "display_order": 410,
                "genres": ["adventure", "comedy", "action"],
                "is_trending": True, "is_latest": True
            },
            {
                "title": "The Night Manager",
                "description": "Currently trending on Disney+ Hotstar. A hotel night manager is recruited by a government agent to infiltrate the inner circle of a ruthless arms dealer.",
                "poster_url": "https://image.tmdb.org/t/p/original/1MccRnw41qQjREuZkovqP2UX1i3.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/2vAOdruqvx9GojXxKi3xVsZZvKU.jpg",
                "rating": 8.7,
                "release_year": 2023,
                "language": "Hindi",
                "duration": "TV Series",
                "cast": "Anil Kapoor, Aditya Roy Kapur, Sobhita Dhulipala",
                "crew": "Director: Sandeep Modi",
                "display_order": 420,
                "genres": ["thriller", "drama", "action"],
                "is_trending": True, "is_latest": True
            },
            {
                "title": "Wednesday",
                "description": "Follows Wednesday Addams' years as a student at Nevermore Academy, as she attempts to master her emerging psychic ability, thwart a monstrous killing spree, and solve the mystery that embroiled her parents.",
                "poster_url": "https://image.tmdb.org/t/p/original/oOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/iHSwvRVsRyxpX7FE7GbviaDvgGZ.jpg",
                "rating": 8.8,
                "release_year": 2022,
                "language": "English",
                "duration": "TV Series",
                "cast": "Jenna Ortega, Gwendoline Christie, Riki Lindhome",
                "crew": "Creators: Alfred Gough, Miles Millar",
                "display_order": 430,
                "genres": ["comedy", "horror", "thriller"],
                "is_popular": True
            },
            {
                "title": "The Last of Us",
                "description": "After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl who may be humanity's last hope.",
                "poster_url": "https://image.tmdb.org/t/p/original/dmo6TYuuJgaYinXBPjrgG9mB5od.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/acevLdSl5I2MK5RYAm7gwAndt1w.jpg",
                "rating": 9.4,
                "release_year": 2023,
                "language": "English",
                "duration": "TV Series",
                "cast": "Pedro Pascal, Bella Ramsey, Gabriel Luna",
                "crew": "Creators: Craig Mazin, Neil Druckmann",
                "display_order": 440,
                "genres": ["drama", "action", "sci-fi"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Squid Game",
                "description": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes.",
                "poster_url": "https://image.tmdb.org/t/p/original/1QdXdRYfktUSONkl1oD5gc6Be0s.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/2meX1nMdScFOoV4370rqHWKmXhY.jpg",
                "rating": 9.1,
                "release_year": 2021,
                "language": "Korean",
                "duration": "TV Series",
                "cast": "Lee Jung-jae, Park Hae-soo, Wi Ha-jun",
                "crew": "Creator: Hwang Dong-hyuk",
                "display_order": 450,
                "genres": ["thriller", "drama", "action"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "The Haunting of Hill House",
                "description": "Flashing between past and present, a fractured family confronts haunting memories of their old home and the terrifying events that drove them from it.",
                "poster_url": "https://image.tmdb.org/t/p/original/38PkhBGRQtmVx2drvPik3F42qHO.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/sNtNXwtEbdw4LaCFxFQwL2Jv4yW.jpg",
                "rating": 9.2,
                "release_year": 2018,
                "language": "English",
                "duration": "TV Series",
                "cast": "Michiel Huisman, Carla Gugino, Timothy Hutton, Elizabeth Reaser",
                "display_order": 460,
                "genres": ["horror", "drama"],
                "crew": "Creator: Mike Flanagan",
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "From",
                "description": "Unraveling the mystery of a nightmarish town that traps everyone who enters, the residents fight to survive while searching for a way out.",
                "poster_url": "https://image.tmdb.org/t/p/original/uV65yaFkw6B4KHXAsBYui0KvJq.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/xLdw1xdHocKYFFvx7w41NchXMfJ.jpg",
                "rating": 7.8,
                "release_year": 2022,
                "language": "English",
                "duration": "TV Series",
                "cast": "Harold Perrineau, Catalina Sandino Moreno, Eion Bailey",
                "crew": "Creator: John Griffin",
                "display_order": 470,
                "genres": ["horror", "thriller"],
                "is_trending": True, "is_popular": True
            },
            {
                "title": "Alice in the Borderland",
                "description": "A group of friends must survive dangerous games in an abandoned Tokyo that has become a ruthless alternate world.",
                "poster_url": "https://m.media-amazon.com/images/I/61BusO1K0hL._AC_UF894,1000_QL80_.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/Ac8ruycRXzgcsndTZFK6ouGA0FA.jpg",
                "rating": 7.7,
                "release_year": 2020,
                "language": "Japanese",
                "duration": "TV Series",
                "cast": "Kento Yamazaki, Tao Tsuchiya, Nijiro Murakami",
                "crew": "Creators: Haro Aso, Shinsuke Sato",
                "display_order": 480,
                "genres": ["thriller", "action", "sci-fi"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Moon Knight",
                "description": "A complex antihero with dissociative identity disorder becomes entangled in a deadly mystery involving Egyptian gods.",
                "poster_url": "https://m.media-amazon.com/images/M/MV5BNDAzNmYwZjgtNDc3YS00ZDMyLTk0MjktMTg4MGNmNGU3MjlhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/iux1vKPT7Vw1AzetZb4Jz6wfYsm.jpg",
                "rating": 7.7,
                "release_year": 2022,
                "language": "English",
                "duration": "TV Series",
                "cast": "Oscar Isaac, Ethan Hawke, May Calamawy",
                "crew": "Creator: Jeremy Slater",
                "display_order": 490,
                "genres": ["action", "adventure", "drama"],
                "is_trending": True, "is_latest": True
            },
            {
                "title": "Dark",
                "description": "A time-travel mystery that follows four interconnected families as they uncover a sinister time loop spanning several generations.",
                "poster_url": "https://image.tmdb.org/t/p/original/dark_poster.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/3jDXL4Xvj3AzDOF6UH1xeyHW8MH.jpg",
                "rating": 9.0,
                "release_year": 2017,
                "language": "German",
                "duration": "TV Series",
                "cast": "Louis Hofmann, Karoline Eichhorn, Lisa Vicari",
                "crew": "Creators: Baran bo Odar, Jantje Friese",
                "display_order": 500,
                "genres": ["drama", "sci-fi", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "Chernobyl",
                "description": "A dramatization of the true story of one of the worst man-made catastrophes in history: the catastrophic nuclear accident at Chernobyl.",
                "poster_url": "https://image.tmdb.org/t/p/original/chernobyl_poster.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/3URK0z9PzpVNJrGE7XOuyy6KFzk.jpg",
                "rating": 9.4,
                "release_year": 2019,
                "language": "English",
                "duration": "TV Series",
                "cast": "Jared Harris, Stellan Skarsgård, Emily Watson",
                "crew": "Creator: Craig Mazin",
                "display_order": 510,
                "genres": ["drama", "thriller"],
                "is_popular": True, "is_top_rated": True
            },
            {
                "title": "The Boroughs",
                "description": "A gritty anthology exploring crime, community, and resilience across different neighborhoods of a modern metropolis.",
                "poster_url": "https://image.tmdb.org/t/p/original/the_boroughs_poster.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/iftYIh1OjJb99EOTHIrDcx59zWb.jpg",
                "rating": 8.2,
                "release_year": 2022,
                "language": "English",
                "duration": "TV Series",
                "cast": "Ensemble Cast",
                "crew": "Creators: Various",
                "display_order": 520,
                "genres": ["drama", "crime"],
                "is_trending": True
            },
            {
                "title": "Spider-Noir",
                "description": "A stylistic, noir-influenced animated series following a masked vigilante who navigates a shadowy multiverse of crime and paradox.",
                "poster_url": "https://image.tmdb.org/t/p/original/spider_noir_poster.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/6t2FvBr9DS8MOq0m5FAwPBCdAW5.jpg",
                "rating": 8.6,
                "release_year": 2024,
                "language": "English",
                "duration": "TV Series",
                "cast": "Voice Cast",
                "crew": "Creators: Creative Studio",
                "display_order": 530,
                "genres": ["action", "adventure", "comedy"],
                "is_latest": True
            },
            {
                "title": "Scam 1992: The Harshad Mehta Story",
                "description": "Set in 1980s and 1990s Bombay, the series follows the meteoric rise and subsequent downfall of Harshad Mehta, a charismatic stockbroker who became known as the \"Bachchan of the BSE.\" Based on the book by Sucheta Dalal and Debashish Basu, it depicts how Mehta masterminded India's biggest financial scam by exploiting loopholes in the banking system, leading to a massive stock market crash and a landmark investigation.",
                "content_type": "series",
                "poster_url": "https://image.tmdb.org/t/p/original/dFTuVCjMMLCZB8mobKSwu5KC2bq.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/tTYP1npvBU90NthceezScfXGiOl.jpg",
                "rating": 9.4,
                "release_year": 2020,
                "language": "Hindi",
                "duration": "1 Season (10 Episodes)",
                "cast": "Pratik Gandhi, Shreya Dhanwanthary, Hemant Kher, Chirag Vohra, Rajat Kapoor, Satish Kaushik, Nikhil Dwivedi, Anant Mahadevan, Sharib Hashmi",
                "crew": "Director: Hansal Mehta, Jai Mehta",
                "display_order": 540,
                "genres": ["drama", "thriller", "biography", "crime"],
                "is_popular": True,
                "is_top_rated": True
            },
            {
                "title": "Farzi",
                "description": "Sunny, a brilliant but disillusioned artist struggling to keep his grandfather's printing press afloat, decides to use his skills to create high-quality counterfeit currency. Along with his best friend Firoz, they plunge into the lucrative and perilous underworld of counterfeiting. Soon, they are caught in a deadly cat-and-mouse game between Michael, a relentless task force officer, and Mansoor, a ruthless gangster running a global smuggling syndicate.",
                "content_type": "series",
                "poster_url": "https://image.tmdb.org/t/p/original/8Y4nn8xevdXGGfk8GN38hnc7Qa6.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/rGkjtv6UdL1ysDmZuBjbNl3PAA1.jpg",
                "rating": 8.4,
                "release_year": 2023,
                "language": "Hindi",
                "duration": "1 Season (8 Episodes)",
                "cast": "Shahid Kapoor, Vijay Sethupathi, Kay Kay Menon, Raashii Khanna, Bhuvan Arora, Amol Palekar, Regina Cassandra, Zakir Hussain, Kubbra Sait",
                "crew": "Director: Raj Nidimoru, Krishna D.K.",
                "display_order": 550,
                "genres": ["action", "drama", "thriller", "comedy", "crime"],
                "is_trending": True,
                "is_popular": True
            },
            {
                "title": "The Family Man",
                "description": "Srikant Tiwari is a middle-class man who seems to lead an ordinary, mundane life. In reality, he is a senior analyst for TASC, a secret espionage wing of the National Investigation Agency. While working under extreme pressure to protect the nation from terrorist threats and high-stakes conspiracies, Srikant must also navigate the everyday challenges of family life, keeping his secret career hidden from his suspicious wife and children.",
                "content_type": "series",
                "poster_url": "https://image.tmdb.org/t/p/original/bv9xrcqcMysqUEJ0sdQd3kUDHPe.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/sAzOPtLtqeveLDncierhahMIIpK.jpg",
                "rating": 8.7,
                "release_year": 2019,
                "language": "Hindi",
                "duration": "2 Seasons (19 Episodes)",
                "cast": "Manoj Bajpayee, Priyamani, Sharib Hashmi, Samantha Ruth Prabhu, Ashlesha Thakur, Vedant Sinha, Shreya Dhanwanthary, Sharad Kelkar, Sunny Hinduja, Neeraj Madhav",
                "crew": "Director: Raj Nidimoru, Krishna D.K., Suparn S. Verma",
                "display_order": 560,
                "genres": ["action", "drama", "thriller", "comedy"],
                "is_popular": True,
                "is_top_rated": True
            },
            {
                "title": "Asur: Welcome to Your Dark Side",
                "description": "Set against the mystical backdrop of Varanasi, this psychological thriller follows Nikhil Nair, a former forensic expert turned teacher, who is called back to the CBI to assist his mentor Dhananjay Rajpoot. Together, they confront a mysterious, brilliant serial killer who uses mythological concepts from Hindu philosophy to justify his brutal murders, claiming to be the incarnation of the demon Kali.",
                "content_type": "series",
                "poster_url": "https://image.tmdb.org/t/p/original/9AZnfGUnPZBBJJDtYk5Uoxw4IMf.jpg",
                "banner_url": "https://image.tmdb.org/t/p/original/eXUr34XTqYaDwyOerFpL6sUOgDL.jpg",
                "rating": 8.5,
                "release_year": 2020,
                "language": "Hindi",
                "duration": "2 Seasons (16 Episodes)",
                "cast": "Arshad Warsi, Barun Sobti, Anupriya Goenka, Riddhi Dogra, Amey Wagh, Sharib Hashmi, Abhishek Chauhan, Meiyang Chang",
                "crew": "Director: Oni Sen",
                "display_order": 570,
                "genres": ["thriller", "drama", "mystery", "crime"],
                "is_popular": True,
                "is_top_rated": True
            }
        ]

        for item in real_media:
            movie = Movie.objects.create(
                title=item['title'],
                description=item['description'],
                content_type=item.get('content_type', 'series' if item['duration'] == 'TV Series' else 'movie'),
                poster_url=item['poster_url'],
                banner_url=item['banner_url'],
                video_url=youtube_trailers.get(item['title'], 'https://www.youtube.com/watch?v=zSWdZAIB5nY'),
                rating=item['rating'],
                release_year=item['release_year'],
                language=item['language'],
                duration=item['duration'],
                is_trending=item.get('is_trending', False),
                is_popular=item.get('is_popular', False),
                is_latest=item.get('is_latest', False),
                is_top_rated=item.get('is_top_rated', False),
                cast=item['cast'],
                crew=item['crew'],
                display_order=item.get('display_order', 0)
            )
            if movie.title in poster_overrides:
                movie.poster_url = poster_overrides[movie.title]
            for g_slug in item['genres']:
                if g_slug in genres_map:
                    movie.genres.add(genres_map[g_slug])
            # Validate banner URLs; poster URLs are overridden explicitly from the provided list.
            def url_ok(url):
                if not url:
                    return False
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                try:
                    with urllib.request.urlopen(req, timeout=8) as res:
                        code = res.getcode()
                        ctype = res.headers.get('Content-Type', '')
                        return code == 200 and ctype.startswith('image')
                except Exception as e:
                    # Retry once with unverified SSL context for hosts with SSL issues
                    try:
                        ctx = ssl._create_unverified_context()
                        with urllib.request.urlopen(req, timeout=8, context=ctx) as res:
                            code = res.getcode()
                            ctype = res.headers.get('Content-Type', '')
                            return code == 200 and ctype.startswith('image')
                    except Exception:
                        return False

            if not url_ok(movie.banner_url):
                movie.banner_url = f"https://placehold.co/1280x720?text={urllib.parse.quote_plus(movie.title)}"
            movie.save()
            created_movies.append(movie)
            
        self.stdout.write(f"Successfully created {len(created_movies)} real movies/series.")
        
        # Create Parent/Child relationships for demonstration
        self.stdout.write("Linking sequels and seasons...")
        
        # 1. Spider-Man Collection
        spiderman_parent = Movie.objects.create(
            title="Spider-Man (MCU) Trilogy",
            description="The complete high-stakes journey of Peter Parker in the Marvel Cinematic Universe, balancing high school life with protecting New York.",
            content_type="movie",
            poster_url="https://static.wikia.nocookie.net/marvelcinematicuniverse/images/1/1d/Spider-Man_No_Way_Home_JP_Poster.jpg/revision/latest/thumbnail/width/360/height/360?cb=20211125071618",
            banner_url="https://image.tmdb.org/t/p/original/tyQo080tijexyUHBvWPwQt26bZa.jpg",
            video_url="https://www.youtube.com/watch?v=JfVOs4VSpmA",
            rating=9.2,
            release_year=2021,
            language="English",
            duration="3 Movies",
            is_trending=True,
            is_popular=True,
            cast="Tom Holland, Zendaya, Jacob Batalon",
            crew="Director: Jon Watts",
            display_order=180
        )
        spiderman_parent.genres.add(genres_map['action'], genres_map['adventure'], genres_map['sci-fi'])
        created_movies.append(spiderman_parent)
        
        sm1 = Movie.objects.create(
            title="Spider-Man: Homecoming",
            description="Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man, and finds himself on the trail of a new menace prowling the skies of New York City.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/45Y6crcltT124S-5Z88gJm3e9a.jpg",
            banner_url="https://image.tmdb.org/t/p/original/fn4n6metrTfXtD9u5cu7oU7Ifw8.jpg",
            video_url="https://www.youtube.com/watch?v=39udgGPyYHI",
            rating=8.5,
            release_year=2017,
            language="English",
            duration="2h 13m",
            cast="Tom Holland, Michael Keaton, Robert Downey Jr., Zendaya",
            crew="Director: Jon Watts",
            parent=spiderman_parent,
            part_number=1,
            part_name="Homecoming"
        )
        sm1.genres.add(genres_map['action'], genres_map['adventure'], genres_map['sci-fi'])
        created_movies.append(sm1)

        sm2 = Movie.objects.create(
            title="Spider-Man: Far From Home",
            description="Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/4q235wzywOU2M4hwvtuiTB0vU7N.jpg",
            banner_url="https://image.tmdb.org/t/p/original/1Ruzn4VnEw0qYJux4T9Y52TjS0s.jpg",
            video_url="https://www.youtube.com/watch?v=Nt9L1jyeSdg",
            rating=8.7,
            release_year=2019,
            language="English",
            duration="2h 9m",
            cast="Tom Holland, Samuel L. Jackson, Jake Gyllenhaal, Zendaya",
            crew="Director: Jon Watts",
            parent=spiderman_parent,
            part_number=2,
            part_name="Far From Home"
        )
        sm2.genres.add(genres_map['action'], genres_map['adventure'], genres_map['sci-fi'])
        created_movies.append(sm2)

        # Find existing No Way Home movie and update it
        try:
            nwh = Movie.objects.get(title="Spider-Man: No Way Home")
            nwh.parent = spiderman_parent
            nwh.part_number = 3
            nwh.part_name = "No Way Home"
            nwh.video_url = "https://www.youtube.com/watch?v=JfVOs4VSpmA"
            nwh.save()
        except Movie.DoesNotExist:
            pass

        # 2. Dune Collection
        dune_parent = Movie.objects.create(
            title="Dune Collection",
            description="The epic saga of Paul Atreides as he navigates the dangerous desert planet of Arrakis and leads the Fremen in a war for the universe.",
            content_type="movie",
            poster_url="https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            banner_url="https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg",
            video_url="https://www.youtube.com/watch?v=Way9Dexny3w",
            rating=9.5,
            release_year=2024,
            language="English",
            duration="2 Movies",
            is_trending=True,
            is_popular=True,
            cast="Timothée Chalamet, Zendaya, Rebecca Ferguson, Oscar Isaac, Josh Brolin",
            crew="Director: Denis Villeneuve",
            display_order=20
        )
        dune_parent.genres.add(genres_map['sci-fi'], genres_map['adventure'], genres_map['action'])
        created_movies.append(dune_parent)

        dune1 = Movie.objects.create(
            title="Dune: Part One",
            description="Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/d5NXSklXkiZt14AL49L4BtZAVXc.jpg",
            banner_url="https://image.tmdb.org/t/p/original/lz7617S53MIZ9O5qGg7G5617oAb.jpg",
            video_url="https://www.youtube.com/watch?v=8g18jFHCLzs",
            rating=9.0,
            release_year=2021,
            language="English",
            duration="2h 35m",
            cast="Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Josh Brolin",
            crew="Director: Denis Villeneuve",
            parent=dune_parent,
            part_number=1,
            part_name="Part One"
        )
        dune1.genres.add(genres_map['sci-fi'], genres_map['adventure'], genres_map['action'])
        created_movies.append(dune1)

        try:
            dune2 = Movie.objects.get(title="Dune: Part Two")
            dune2.parent = dune_parent
            dune2.part_number = 2
            dune2.part_name = "Part Two"
            dune2.video_url = "https://www.youtube.com/watch?v=Way9Dexny3w"
            dune2.save()
        except Movie.DoesNotExist:
            pass

        # 3. Avatar Collection
        avatar_parent = Movie.objects.create(
            title="Avatar Collection",
            description="Enter the world of Pandora, where a paraplegic Marine embarks on a unique journey of adventure and love, fighting to protect the land he learns to call home.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/kyeqWJfphcuFF0TC0o4lY56u7Ls.jpg",
            banner_url="https://image.tmdb.org/t/p/original/qnzQm0PCVnSyv1dqpVmRgMWHbLD.jpg",
            video_url="https://www.youtube.com/watch?v=d9MyW72ELq0",
            rating=9.0,
            release_year=2022,
            language="English",
            duration="2 Movies",
            is_trending=True,
            is_popular=True,
            cast="Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang",
            crew="Director: James Cameron",
            display_order=160
        )
        avatar_parent.genres.add(genres_map['sci-fi'], genres_map['adventure'], genres_map['action'])
        created_movies.append(avatar_parent)

        avatar1 = Movie.objects.create(
            title="Avatar",
            description="A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/kyeqWJfphcuFF0TC0o4lY56u7Ls.jpg",
            banner_url="https://image.tmdb.org/t/p/original/vL526wSBrjSPV67j2RjUuSyjKga.jpg",
            video_url="https://www.youtube.com/watch?v=5PSNL1q3fy8",
            rating=8.9,
            release_year=2009,
            language="English",
            duration="2h 42m",
            cast="Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang",
            crew="Director: James Cameron",
            parent=avatar_parent,
            part_number=1,
            part_name="Avatar"
        )
        avatar1.genres.add(genres_map['sci-fi'], genres_map['adventure'], genres_map['action'])
        created_movies.append(avatar1)

        try:
            avatar2 = Movie.objects.get(title="Avatar: The Way of Water")
            avatar2.parent = avatar_parent
            avatar2.part_number = 2
            avatar2.part_name = "The Way of Water"
            avatar2.video_url = "https://www.youtube.com/watch?v=d9MyW72ELq0"
            avatar2.save()
        except Movie.DoesNotExist:
            pass

        # 4. Avengers Collection
        avengers_parent = Movie.objects.create(
            title="Avengers Collection",
            description="Earth's Mightiest Heroes stand together to battle the threats that no single hero could withstand, culminating in the battle against the Mad Titan, Thanos.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/or7PzF6ZRkJGBlPp6oom5QYQ2yQ.jpg",
            banner_url="https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
            video_url="https://www.youtube.com/watch?v=TcMBFSGVi1c",
            rating=9.5,
            release_year=2019,
            language="English",
            duration="4 Movies",
            is_trending=True,
            is_popular=True,
            cast="Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth, Scarlett Johansson",
            crew="Directors: Joss Whedon, Anthony Russo, Joe Russo",
            display_order=260
        )
        avengers_parent.genres.add(genres_map['action'], genres_map['sci-fi'], genres_map['adventure'])
        created_movies.append(avengers_parent)

        av1 = Movie.objects.create(
            title="The Avengers",
            description="Earth's mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/RYMX2wc76YgXeRIyw6d6Z4SAjG.jpg",
            banner_url="https://image.tmdb.org/t/p/original/9BBTo6m1X2p4d24W2r2kceJ76J8.jpg",
            video_url="https://www.youtube.com/watch?v=eOrNdByGMv8",
            rating=8.8,
            release_year=2012,
            language="English",
            duration="2h 23m",
            cast="Robert Downey Jr., Chris Evans, Scarlett Johansson, Mark Ruffalo",
            crew="Director: Joss Whedon",
            parent=avengers_parent,
            part_number=1,
            part_name="The Avengers"
        )
        av1.genres.add(genres_map['action'], genres_map['sci-fi'], genres_map['adventure'])
        created_movies.append(av1)

        av2 = Movie.objects.create(
            title="Avengers: Age of Ultron",
            description="When Tony Stark and Bruce Banner try to jump-start a dormant peacekeeping program called Ultron, things go horribly wrong and it's up to Earth's mightiest heroes to stop the villainous Ultron from enacting his terrible plan.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/4ssDuvj0MKmQki84I2Jrzq5zVaa.jpg",
            banner_url="https://image.tmdb.org/t/p/original/87Wwquby7w7kZ77t465gA878401.jpg",
            video_url="https://www.youtube.com/watch?v=tmeOjFno6Do",
            rating=8.5,
            release_year=2015,
            language="English",
            duration="2h 21m",
            cast="Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
            crew="Director: Joss Whedon",
            parent=avengers_parent,
            part_number=2,
            part_name="Age of Ultron"
        )
        av2.genres.add(genres_map['action'], genres_map['sci-fi'], genres_map['adventure'])
        created_movies.append(av2)

        av3 = Movie.objects.create(
            title="Avengers: Infinity War",
            description="The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/7WsyChwLEAx4xdIFqRxyz78V2si.jpg",
            banner_url="https://image.tmdb.org/t/p/original/bOGkgm7gHn171t4t72nqpj1nPEb.jpg",
            video_url="https://www.youtube.com/watch?v=QwievZ1Tx-8",
            rating=9.3,
            release_year=2018,
            language="English",
            duration="2h 29m",
            cast="Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans",
            crew="Directors: Anthony Russo, Joe Russo",
            parent=avengers_parent,
            part_number=3,
            part_name="Infinity War"
        )
        av3.genres.add(genres_map['action'], genres_map['sci-fi'], genres_map['adventure'])
        created_movies.append(av3)

        try:
            av4 = Movie.objects.get(title="Avengers: Endgame")
            av4.parent = avengers_parent
            av4.part_number = 4
            av4.part_name = "Endgame"
            av4.video_url = "https://www.youtube.com/watch?v=TcMBFSGVi1c"
            av4.save()
        except Movie.DoesNotExist:
            pass

        # 5. The Conjuring Trilogy
        conjuring_parent = Movie.objects.create(
            title="The Conjuring Trilogy",
            description="The chilling investigations of paranormal experts Ed and Lorraine Warren as they battle demonic entities and haunted houses.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
            banner_url="https://image.tmdb.org/t/p/original/ecKQlAEG95k62SMGhvX83oEqANK.jpg",
            video_url="https://www.youtube.com/watch?v=k10ETZ42q5o",
            rating=8.7,
            release_year=2021,
            language="English",
            duration="3 Movies",
            is_trending=True,
            is_popular=True,
            cast="Vera Farmiga, Patrick Wilson",
            crew="Directors: James Wan, Michael Chaves",
            display_order=130
        )
        conjuring_parent.genres.add(genres_map['horror'], genres_map['thriller'])
        created_movies.append(conjuring_parent)

        try:
            cj1 = Movie.objects.get(title="The Conjuring")
            cj1.parent = conjuring_parent
            cj1.part_number = 1
            cj1.part_name = "The Conjuring"
            cj1.video_url = "https://www.youtube.com/watch?v=k10ETZ42q5o"
            cj1.save()
        except Movie.DoesNotExist:
            pass

        cj2 = Movie.objects.create(
            title="The Conjuring 2",
            description="Ed and Lorraine Warren travel to North London to help a single mother raising four children alone in a house plagued by a supernatural spirit.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/71727aVGR-LeNcwcUawssDsRp2X.jpg",
            banner_url="https://image.tmdb.org/t/p/original/q9m59lK28yO4VWh3q4V30o86rUa.jpg",
            video_url="https://www.youtube.com/watch?v=VFsMuDlimuA",
            rating=8.6,
            release_year=2016,
            language="English",
            duration="2h 14m",
            cast="Vera Farmiga, Patrick Wilson, Frances O'Connor",
            crew="Director: James Wan",
            parent=conjuring_parent,
            part_number=2,
            part_name="The Conjuring 2"
        )
        cj2.genres.add(genres_map['horror'], genres_map['thriller'])
        created_movies.append(cj2)

        cj3 = Movie.objects.create(
            title="The Conjuring: The Devil Made Me Do It",
            description="A chilling story of terror, murder and unknown evil that shocked even experienced real-life paranormal investigators Ed and Lorraine Warren.",
            content_type="movie",
            poster_url="https://image.tmdb.org/t/p/original/xbSu194Lh1VvG25v5a7t67v9C1k.jpg",
            banner_url="https://image.tmdb.org/t/p/original/qi6v4x7jG7XnPEU4r792345O.jpg",
            video_url="https://www.youtube.com/watch?v=h9Q4zZsOPTU",
            rating=8.2,
            release_year=2021,
            language="English",
            duration="1h 52m",
            cast="Vera Farmiga, Patrick Wilson, Ruairi O'Connor",
            crew="Director: Michael Chaves",
            parent=conjuring_parent,
            part_number=3,
            part_name="The Devil Made Me Do It"
        )
        cj3.genres.add(genres_map['horror'], genres_map['thriller'])
        created_movies.append(cj3)

        # 6. TV Show Seasons: Stranger Things

        try:
            st_parent = Movie.objects.get(title="Stranger Things")
            st_parent.duration = "5 Seasons"
            st_parent.video_url = "https://www.youtube.com/watch?v=yQEondeGvKo"
            st_parent.save()
            
            # Season 1
            sts1 = Movie.objects.create(
                title="Stranger Things: Season 1",
                description="When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
                content_type="series",
                poster_url="https://image.tmdb.org/t/p/original/uOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
                banner_url="https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                video_url="https://www.youtube.com/watch?v=b9EkMc79ZSU",
                rating=9.2,
                release_year=2016,
                language="English",
                duration="8 Episodes",
                cast="Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour",
                crew="Creators: The Duffer Brothers",
                parent=st_parent,
                part_number=1,
                part_name="Season 1"
            )
            sts1.genres.add(genres_map['horror'], genres_map['sci-fi'], genres_map['thriller'])
            created_movies.append(sts1)
            
            # Season 2
            sts2 = Movie.objects.create(
                title="Stranger Things: Season 2",
                description="It's 1984 and the citizens of Hawkins, Indiana are still reeling from the horrors of the Demogorgon and the secrets of Hawkins Lab. Will Byers has been rescued from the Upside Down but a bigger, sinister entity still threatens those who survived.",
                content_type="series",
                poster_url="https://image.tmdb.org/t/p/original/l9zV3X8uMoxbC23iL7lUu8H1Jz4.jpg",
                banner_url="https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                video_url="https://www.youtube.com/watch?v=vgS2L7WPIO4",
                rating=9.0,
                release_year=2017,
                language="English",
                duration="9 Episodes",
                cast="Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour, Sadie Sink",
                crew="Creators: The Duffer Brothers",
                parent=st_parent,
                part_number=2,
                part_name="Season 2"
            )
            sts2.genres.add(genres_map['horror'], genres_map['sci-fi'], genres_map['thriller'])
            created_movies.append(sts2)
            
            # Season 3
            sts3 = Movie.objects.create(
                title="Stranger Things: Season 3",
                description="Budding romance, a new mall, and a menacing threat looming in the summer heat of 1985 in Hawkins. Old and new enemies are reminding everyone that evil never ends; it explains and evolves.",
                content_type="series",
                poster_url="https://image.tmdb.org/t/p/original/x2Lw33d2v2ggEQEQ8122vJ7n.jpg",
                banner_url="https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                video_url="https://www.youtube.com/watch?v=YEG3bmU_WaI",
                rating=8.9,
                release_year=2019,
                language="English",
                duration="8 Episodes",
                cast="Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour, Dacre Montgomery",
                crew="Creators: The Duffer Brothers",
                parent=st_parent,
                part_number=3,
                part_name="Season 3"
            )
            sts3.genres.add(genres_map['horror'], genres_map['sci-fi'], genres_map['thriller'])
            created_movies.append(sts3)
 
            # Season 4
            sts4 = Movie.objects.create(
                title="Stranger Things: Season 4",
                description="It's been six months since the Battle of Starcourt, which brought terror and destruction to Hawkins. Struggling with the aftermath, our group of friends are separated for the first time – and navigating the complexities of high school hasn't made things any easier.",
                content_type="series",
                poster_url="https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                banner_url="https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                video_url="https://www.youtube.com/watch?v=yQEondeGvKo",
                rating=9.3,
                release_year=2022,
                language="English",
                duration="9 Episodes",
                cast="Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour, Joseph Quinn",
                crew="Creators: The Duffer Brothers",
                parent=st_parent,
                part_number=4,
                part_name="Season 4"
            )
            sts4.genres.add(genres_map['horror'], genres_map['sci-fi'], genres_map['thriller'])
            created_movies.append(sts4)
            
            # Season 5
            sts5 = Movie.objects.create(
                title="Stranger Things: Season 5",
                description="The final season of the epic saga, as the gang confronts the Upside Down once and for all.",
                content_type="series",
                poster_url="https://image.tmdb.org/t/p/original/uOOtwVbSr4QDjAGIifLDwpb2Pdl.jpg",
                banner_url="https://image.tmdb.org/t/p/original/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
                video_url="https://www.youtube.com/watch?v=b1BvO8Zp3wY",
                rating=9.6,
                release_year=2025,
                language="English",
                duration="8 Episodes",
                cast="Millie Bobby Brown, Finn Wolfhard, Winona Ryder, David Harbour",
                crew="Creators: The Duffer Brothers",
                parent=st_parent,
                part_number=5,
                part_name="Season 5"
            )
            sts5.genres.add(genres_map['horror'], genres_map['sci-fi'], genres_map['thriller'])
            created_movies.append(sts5)
        except Movie.DoesNotExist:
            pass

        self.stdout.write("Creating users...")
        # Superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@cineverse.com', 'admin123')
            self.stdout.write("Created superuser: admin / admin123")
        else:
            admin_user = User.objects.get(username='admin')

        # Marcus
        marcus_user, created = User.objects.get_or_create(username='marcus', defaults={
            'email': 'marcus@cineverse.com',
            'first_name': 'Marcus',
            'last_name': 'Vance',
        })
        if created:
            marcus_user.set_password('marcus123')
            marcus_user.save()
            self.stdout.write("Created user: marcus / marcus123")
            
        profile, _ = UserProfile.objects.get_or_create(user=marcus_user)
        profile.subscription_plan = 'Premium'
        profile.favorite_genres.add(genres_map['sci-fi'], genres_map['action'])
        # Add some watchlist movies from created movies
        if len(created_movies) > 5:
            profile.watchlist.add(created_movies[0], created_movies[1], created_movies[2])
            profile.favorites.add(created_movies[2], created_movies[3], created_movies[4])
        profile.save()
        
        # Watch history for Marcus
        if len(created_movies) > 8:
            WatchHistory.objects.create(user=marcus_user, movie=created_movies[5], progress=75)
            WatchHistory.objects.create(user=marcus_user, movie=created_movies[6], progress=50)
            WatchHistory.objects.create(user=marcus_user, movie=created_movies[7], progress=40)
            WatchHistory.objects.create(user=marcus_user, movie=created_movies[8], progress=95)
        
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.subscription_plan = 'Premium'
        admin_profile.save()
        if len(created_movies) > 2:
            WatchHistory.objects.create(user=admin_user, movie=created_movies[0], progress=100)
            WatchHistory.objects.create(user=admin_user, movie=created_movies[1], progress=20)
            
        self.stdout.write("Seeding complete! Admin credentials: admin / admin123. Marcus credentials: marcus / marcus123.")
