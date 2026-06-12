from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.db.models import Q, Max
from .models import Genre, Movie, UserProfile, WatchHistory
import json

def serialize_movie(m, watchlist_ids=set(), favorites_ids=set()):
    if not m:
        return None
    return {
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'content_type': m.content_type,
        'poster_url': m.poster_url,
        'banner_url': m.banner_url,
        'video_url': m.video_url,
        'rating': float(m.rating) if m.rating is not None else 0.0,
        'release_year': m.release_year,
        'language': m.language,
        'duration': m.duration,
        'cast': m.cast,
        'crew': m.crew,
        'display_order': m.display_order,
        'genres': [g.slug for g in m.genres.all()],
        'in_watchlist': m.id in watchlist_ids,
        'in_favorites': m.id in favorites_ids,
        'is_trending': m.is_trending,
        'is_popular': m.is_popular,
        'is_latest': m.is_latest,
        'is_top_rated': m.is_top_rated,
    }

def serialize_genre(g):
    if not g:
        return None
    return {
        'id': g.id,
        'name': g.name,
        'slug': g.slug
    }

@never_cache
def home(request):
    featured_movie = Movie.objects.filter(is_trending=True).order_by('display_order').first()
    if not featured_movie:
        featured_movie = Movie.objects.order_by('display_order').first()

    trending_movies = Movie.objects.filter(is_trending=True).order_by('display_order')
    popular_movies = Movie.objects.filter(is_popular=True).order_by('display_order')
    latest_movies = Movie.objects.filter(is_latest=True).order_by('display_order')
    top_rated_movies = Movie.objects.filter(is_top_rated=True).order_by('display_order')

    continue_watching = []
    recommended_movies = Movie.objects.all()[:6]
    show_genre_modal = False
    all_genres = Genre.objects.all()

    watchlist_ids = set()
    favorites_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))
        continue_watching = WatchHistory.objects.filter(user=request.user).select_related('movie')[:4]
        fav_genres = request.user.profile.favorite_genres.all()
        if fav_genres.exists():
            recommended_movies = Movie.objects.filter(genres__in=fav_genres).distinct()
        else:
            recommended_movies = Movie.objects.all()[:6]
        
        show_genre_modal = request.session.pop('show_genre_signup_modal', False)
        if show_genre_modal or not fav_genres.exists():
            show_genre_modal = True

    all_movies = Movie.objects.all().order_by('display_order').prefetch_related('genres')

    payload = {
        'featured_movie': serialize_movie(featured_movie, watchlist_ids, favorites_ids),
        'trending_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in trending_movies],
        'popular_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in popular_movies],
        'latest_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in latest_movies],
        'top_rated_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in top_rated_movies],
        'continue_watching': [{
            'movie': serialize_movie(item.movie, watchlist_ids, favorites_ids),
            'progress': item.progress
        } for item in continue_watching],
        'recommended_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in recommended_movies],
        'show_genre_modal': show_genre_modal,
        'all_genres': [serialize_genre(g) for g in all_genres],
        'all_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in all_movies],
    }

    context = {
        'page_name': 'home',
        'title': 'Home',
        'payload_json': json.dumps(payload),
    }
    return render(request, 'cine_verse/react_index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password."
            
    payload = {'error': error}
    context = {
        'page_name': 'login',
        'title': 'Sign In',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        subscription_plan = request.POST.get('subscription_plan', 'Basic')
        
        if User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = user.profile
            profile.subscription_plan = subscription_plan
            profile.save()
            
            request.session['show_genre_signup_modal'] = True
            login(request, user)
            return redirect('home')
            
    payload = {'error': error}
    context = {
        'page_name': 'register',
        'title': 'Register',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@never_cache
def dashboard(request):
    profile = request.user.profile
    watchlist = list(profile.watchlist.all())
    favorites = list(profile.favorites.all())
    
    if profile.watchlist_order:
        try:
            order_ids = [int(x) for x in profile.watchlist_order.split(',') if x.strip()]
            order_map = {id_: index for index, id_ in enumerate(order_ids)}
            watchlist.sort(key=lambda m: order_map.get(m.id, len(order_ids) + m.id))
        except Exception:
            pass

    if profile.favorites_order:
        try:
            order_ids = [int(x) for x in profile.favorites_order.split(',') if x.strip()]
            order_map = {id_: index for index, id_ in enumerate(order_ids)}
            favorites.sort(key=lambda m: order_map.get(m.id, len(order_ids) + m.id))
        except Exception:
            pass
            
    continue_watching = WatchHistory.objects.filter(user=request.user).select_related('movie')[:4]
    
    total_watched = WatchHistory.objects.filter(user=request.user).count()
    time_watched_hours = int(total_watched * 1.8)
    time_watched_mins = int((total_watched * 1.8 - time_watched_hours) * 60)
    time_watched_str = f"{time_watched_hours}h {time_watched_mins}m"
    
    if total_watched > 10:
        global_ranking = "Top 5%"
    elif total_watched > 5:
        global_ranking = "Top 15%"
    else:
        global_ranking = "Top 50%"
        
    watchlist_ids = set(profile.watchlist.values_list('id', flat=True))
    favorites_ids = set(profile.favorites.values_list('id', flat=True))

    payload = {
        'watchlist': [serialize_movie(m, watchlist_ids, favorites_ids) for m in watchlist],
        'favorites': [serialize_movie(m, watchlist_ids, favorites_ids) for m in favorites],
        'continue_watching': [{
            'movie': serialize_movie(item.movie, watchlist_ids, favorites_ids),
            'progress': item.progress
        } for item in continue_watching],
        'movies_watched_count': total_watched,
        'time_watched_str': time_watched_str,
        'global_ranking': global_ranking,
        'profile': {
            'subscription_plan': profile.subscription_plan,
            'favorite_genres': [g.name for g in profile.favorite_genres.all()]
        }
    }
    context = {
        'page_name': 'dashboard',
        'title': 'User Dashboard',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def movie_list(request):
    movies = Movie.objects.all()
    
    content_type = request.GET.get('content_type', 'all')
    genre_slug = request.GET.get('genre')
    language = request.GET.get('language')
    rating = request.GET.get('rating')
    year = request.GET.get('year')
    q = request.GET.get('q')
    sort = request.GET.get('sort', 'popularity')

    if content_type == 'movie':
        movies = movies.filter(content_type='movie')
    elif content_type == 'series':
        movies = movies.filter(content_type='series')
    
    if q:
        movies = movies.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if genre_slug:
        movies = movies.filter(genres__slug=genre_slug)
    if language:
        movies = movies.filter(language=language)
    if rating:
        movies = movies.filter(rating__gte=float(rating))
    if year:
        movies = movies.filter(release_year=int(year))
        
    genres = Genre.objects.all()
    languages = Movie.objects.values_list('language', flat=True).distinct()
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    watchlist_ids = set()
    favorites_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))

    all_movies_list = Movie.objects.all().order_by('display_order').prefetch_related('genres')

    payload = {
        'all_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in all_movies_list],
        'genres': [serialize_genre(g) for g in genres],
        'languages': list(filter(None, languages)),
        'years': list(filter(None, years)),
        'selected_genre': genre_slug or '',
        'selected_language': language or '',
        'selected_rating': rating or '0',
        'selected_year': year or '',
        'search_query': q or '',
        'selected_content_type': content_type,
        'selected_sort': sort,
    }
    context = {
        'page_name': 'movie_list',
        'title': 'Explore Movies & Series',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    primary_genre = movie.genres.first()
    if primary_genre:
        similar_movies = Movie.objects.filter(genres=primary_genre).exclude(id=movie.id).distinct()[:8]
    else:
        similar_movies = Movie.objects.filter(genres__in=movie.genres.all()).exclude(id=movie.id).distinct()[:8]
    
    in_watchlist = False
    in_favorites = False
    watchlist_ids = set()
    favorites_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))
        in_watchlist = movie.id in watchlist_ids
        in_favorites = movie.id in favorites_ids
        
    cast_list = [c.strip() for c in movie.cast.split(',') if c.strip()]
    crew_list = [c.strip() for c in movie.crew.split(',') if c.strip()]
        
    payload = {
        'movie': serialize_movie(movie, watchlist_ids, favorites_ids),
        'similar_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in similar_movies],
        'in_watchlist': in_watchlist,
        'in_favorites': in_favorites,
        'cast_list': cast_list,
        'crew_list': crew_list,
    }
    context = {
        'page_name': 'movie_detail',
        'title': movie.title,
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

@login_required
def watch_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    history, created = WatchHistory.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        history.save()  # update watched_at timestamp
    
    related_movies = Movie.objects.filter(genres__in=movie.genres.all()).exclude(id=movie.id).distinct()[:4]
    if not related_movies.exists():
        related_movies = Movie.objects.exclude(id=movie.id)[:4]
        
    watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
    favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))

    payload = {
        'movie': serialize_movie(movie, watchlist_ids, favorites_ids),
        'history': {
            'progress': history.progress
        },
        'related_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in related_movies],
    }
    context = {
        'page_name': 'watch',
        'title': f'Now Playing: {movie.title}',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

@login_required
@csrf_exempt
def update_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movie_id = data.get('movie_id')
            progress = int(data.get('progress', 0))
            
            movie = get_object_or_404(Movie, id=movie_id)
            history, created = WatchHistory.objects.get_or_create(user=request.user, movie=movie)
            history.progress = min(max(progress, 0), 100)
            history.save()
            return JsonResponse({'status': 'success', 'progress': history.progress})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
@never_cache
def get_continue_watching(request):
    try:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))
        continue_watching = WatchHistory.objects.filter(user=request.user).select_related('movie')[:4]
        data = [{
            'movie': serialize_movie(item.movie, watchlist_ids, favorites_ids),
            'progress': item.progress
        } for item in continue_watching]
        return JsonResponse({'status': 'success', 'continue_watching': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@csrf_exempt
def toggle_watchlist(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        profile = request.user.profile
        if profile.watchlist.filter(id=movie.id).exists():
            profile.watchlist.remove(movie)
            added = False
        else:
            profile.watchlist.add(movie)
            added = True
        return JsonResponse({'status': 'success', 'added': added})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt
def toggle_favorite(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        profile = request.user.profile
        if profile.favorites.filter(id=movie.id).exists():
            profile.favorites.remove(movie)
            added = False
        else:
            profile.favorites.add(movie)
            added = True
        return JsonResponse({'status': 'success', 'added': added})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt
def user_reorder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reorder_type = data.get('type') # 'watchlist' or 'favorites'
            movie_ids = data.get('movie_ids', [])
            
            # Sanitize and convert list of IDs to comma-separated string
            id_str = ','.join(str(int(x)) for x in movie_ids)
            
            profile = request.user.profile
            if reorder_type == 'watchlist':
                profile.watchlist_order = id_str
                profile.save()
            elif reorder_type == 'favorites':
                profile.favorites_order = id_str
                profile.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def profile_view(request):
    profile = request.user.profile
    success_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        favorite_genre_ids = request.POST.getlist('favorite_genres')
        avatar_url = request.POST.get('avatar_url')
        
        request.user.username = username
        request.user.email = email
        request.user.save()
        
        profile.favorite_genres.set(favorite_genre_ids)
        if avatar_url:
            profile.avatar_url = avatar_url
        profile.save()
        success_message = "Profile updated successfully!"
        
    genres = Genre.objects.all()
    watch_history = WatchHistory.objects.filter(user=request.user).select_related('movie')
    watchlist_ids = set(profile.watchlist.values_list('id', flat=True))
    favorites_ids = set(profile.favorites.values_list('id', flat=True))

    payload = {
        'profile': {
            'username': request.user.username,
            'email': request.user.email,
            'avatar_url': profile.avatar_url,
            'favorite_genres': [g.id for g in profile.favorite_genres.all()]
        },
        'genres': [serialize_genre(g) for g in genres],
        'watch_history': [{
            'movie': serialize_movie(item.movie, watchlist_ids, favorites_ids),
            'progress': item.progress
        } for item in watch_history],
        'success_message': success_message
    }
    context = {
        'page_name': 'profile',
        'title': 'Profile Settings',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

@login_required
def subscription_plans(request):
    profile = request.user.profile
    success_message = None
    
    if request.method == 'POST':
        plan = request.POST.get('subscription_plan')
        if plan in ['Basic', 'Standard', 'Premium']:
            profile.subscription_plan = plan
            profile.save()
            success_message = f"Subscription successfully updated to {plan}!"
            
    payload = {
        'profile': {
            'subscription_plan': profile.subscription_plan
        },
        'success_message': success_message
    }
    context = {
        'page_name': 'subscription',
        'title': 'Plans & Pricing',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def admin_dashboard(request):
    # For high-fidelity demo purposes, we will allow anyone to view or mock it,
    # but check superuser flag and display stats of users, movies, and simulated revenue
    total_users = User.objects.count()
    total_movies = Movie.objects.count()
    
    # Calculate mock revenue
    revenue = 0
    for p in UserProfile.objects.all():
        if p.subscription_plan == 'Basic':
            revenue += 8.99
        elif p.subscription_plan == 'Standard':
            revenue += 13.99
        elif p.subscription_plan == 'Premium':
            revenue += 19.99
            
    users = User.objects.all().select_related('profile')
    
    # Get active filters (movies and series separated, with genre filtering)
    selected_content_type = request.GET.get('content_type', 'movie')
    selected_genre_id = request.GET.get('genre', '')
    
    movies = Movie.objects.filter(content_type=selected_content_type)
    if selected_genre_id:
        movies = movies.filter(genres__id=int(selected_genre_id))
        
    movies = movies.order_by('display_order').prefetch_related('genres')
    genres = Genre.objects.all()
    
    watchlist_ids = set()
    favorites_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))

    payload = {
        'total_users': total_users,
        'total_movies': total_movies,
        'monthly_revenue': round(revenue, 2),
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'subscription_plan': u.profile.subscription_plan,
            'avatar_url': u.profile.avatar_url,
            'date_joined': u.date_joined.strftime('%b %d, %Y')
        } for u in users],
        'movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in movies],
        'genres': [serialize_genre(g) for g in genres],
        'selected_content_type': selected_content_type,
        'selected_genre_id': int(selected_genre_id) if selected_genre_id else None,
    }
    context = {
        'page_name': 'admin_dashboard',
        'title': 'Admin Control Panel',
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

def search_results(request):
    q = request.GET.get('q', '')
    genre_slug = request.GET.get('genre')
    language = request.GET.get('language')
    rating = request.GET.get('rating')
    year = request.GET.get('year')
    category = request.GET.get('category', 'all')
    
    movies = Movie.objects.none()
    if q:
        movies = Movie.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))

    all_q_movies = movies

    if category == 'movies':
        movies = movies.filter(content_type='movie')
    elif category == 'tv':
        movies = movies.filter(content_type='series')

    # Apply other filters
    if q and genre_slug:
        movies = movies.filter(genres__slug=genre_slug)
    if q and language:
        movies = movies.filter(language=language)
    if q and rating:
        movies = movies.filter(rating__gte=float(rating))
    if q and year:
        movies = movies.filter(release_year=int(year))
        
    genres = Genre.objects.all()
    languages = Movie.objects.values_list('language', flat=True).distinct()
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    trending_searches = Movie.objects.filter(is_trending=True)[:5]
    if not trending_searches.exists():
        trending_searches = Movie.objects.all()[:5]
        
    total_count = movies.distinct().count() if q else 0
    movie_count = all_q_movies.filter(content_type='movie').distinct().count() if q else 0
    tv_count = all_q_movies.filter(content_type='series').distinct().count() if q else 0
    
    watchlist_ids = set()
    favorites_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
        favorites_ids = set(request.user.profile.favorites.values_list('id', flat=True))

    all_movies_list = Movie.objects.all().order_by('display_order').prefetch_related('genres')

    payload = {
        'all_movies': [serialize_movie(m, watchlist_ids, favorites_ids) for m in all_movies_list],
        'genres': [serialize_genre(g) for g in genres],
        'languages': list(filter(None, languages)),
        'years': list(filter(None, years)),
        'selected_genre': genre_slug or '',
        'selected_language': language or '',
        'selected_rating': rating or '0',
        'selected_year': year or '',
        'search_query': q or '',
        'selected_content_type': 'movie' if category == 'movies' else ('series' if category == 'tv' else 'all'),
        'selected_sort': 'popularity',
        'trending_searches': [serialize_movie(m, watchlist_ids, favorites_ids) for m in trending_searches],
        'total_count': total_count,
        'movie_count': movie_count,
        'tv_count': tv_count,
    }
    context = {
        'page_name': 'search_results',
        'title': f"Search Results: {q}",
        'payload_json': json.dumps(payload)
    }
    return render(request, 'cine_verse/react_index.html', context)

@login_required
def react_discover(request):
    # Route react_discover to movie_list context
    return movie_list(request)

@login_required
@csrf_exempt
def save_genres(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            genre_ids = data.get('genre_ids', [])
            
            # Enforce max 4
            if len(genre_ids) > 4:
                return JsonResponse({'status': 'error', 'message': 'You can select up to 4 genres.'}, status=400)
                
            profile = request.user.profile
            profile.favorite_genres.set(genre_ids)
            profile.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def admin_add_movie(request):
    if not (request.user.is_staff or request.user.is_superuser or request.user.username == 'admin'):
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            content_type = request.POST.get('content_type', 'movie')
            poster_url = request.POST.get('poster_url')
            banner_url = request.POST.get('banner_url')
            video_url = request.POST.get('video_url', 'https://www.w3schools.com/html/mov_bbb.mp4')
            rating = float(request.POST.get('rating', 0.0))
            release_year = int(request.POST.get('release_year', 2024))
            language = request.POST.get('language', 'English')
            duration = request.POST.get('duration', '2h 15m')
            
            is_trending = request.POST.get('is_trending') in ['true', 'on', '1', True]
            is_popular = request.POST.get('is_popular') in ['true', 'on', '1', True]
            is_latest = request.POST.get('is_latest') in ['true', 'on', '1', True]
            is_top_rated = request.POST.get('is_top_rated') in ['true', 'on', '1', True]
            
            cast = request.POST.get('cast', '')
            crew = request.POST.get('crew', 'Director: John Doe')
            genre_ids = request.POST.getlist('genres')
            
            # Find next display order
            max_order = Movie.objects.aggregate(Max('display_order'))['display_order__max']
            display_order = (max_order or 0) + 10
            
            movie = Movie.objects.create(
                title=title,
                description=description,
                content_type=content_type,
                poster_url=poster_url,
                banner_url=banner_url,
                video_url=video_url,
                rating=rating,
                release_year=release_year,
                language=language,
                duration=duration,
                is_trending=is_trending,
                is_popular=is_popular,
                is_latest=is_latest,
                is_top_rated=is_top_rated,
                cast=cast,
                crew=crew,
                display_order=display_order
            )
            
            if genre_ids:
                for gid in genre_ids:
                    try:
                        genre = Genre.objects.get(id=int(gid))
                        movie.genres.add(genre)
                    except (ValueError, Genre.DoesNotExist):
                        pass
                        
            return redirect('admin_dashboard')
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f"Error adding title: {str(e)}"}, status=400)
            
            # Render dashboard with error message
            total_users = User.objects.count()
            total_movies = Movie.objects.count()
            revenue = 0
            for p in UserProfile.objects.all():
                if p.subscription_plan == 'Basic': revenue += 8.99
                elif p.subscription_plan == 'Standard': revenue += 13.99
                elif p.subscription_plan == 'Premium': revenue += 19.99
            users = User.objects.all().select_related('profile')
            movies = Movie.objects.all().order_by('display_order')
            genres = Genre.objects.all()
            return render(request, 'cine_verse/admin_dashboard.html', {
                'total_users': total_users,
                'total_movies': total_movies,
                'monthly_revenue': round(revenue, 2),
                'users': users,
                'movies': movies,
                'genres': genres,
                'error': f"Error adding title: {str(e)}"
            })
            
    return redirect('admin_dashboard')


@login_required
@csrf_exempt
def admin_delete_movie(request, movie_id):
    if not (request.user.is_staff or request.user.is_superuser or request.user.username == 'admin'):
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=400)


@login_required
@csrf_exempt
def admin_reorder_movie(request):
    if not (request.user.is_staff or request.user.is_superuser or request.user.username == 'admin'):
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Support drag list reordering
            if 'movie_ids' in data:
                movie_ids = data.get('movie_ids', [])
                movies = Movie.objects.filter(id__in=movie_ids)
                movie_map = {m.id: m for m in movies}
                for index, m_id in enumerate(movie_ids):
                    m_id = int(m_id)
                    if m_id in movie_map:
                        movie_map[m_id].display_order = (index + 1) * 10
                        movie_map[m_id].save()
                return JsonResponse({'status': 'success'})
            
            # Direction-based fallback reordering
            movie_id = data.get('movie_id')
            direction = data.get('direction') # 'up' or 'down'
            
            # Active filter context from the front-end
            content_type = data.get('content_type', 'movie')
            genre_id = data.get('genre_id')
            
            movie = get_object_or_404(Movie, id=movie_id)
            
            # Retrieve queryset filtered by the exact content type & genre context
            movies_qs = Movie.objects.filter(content_type=content_type)
            if genre_id:
                movies_qs = movies_qs.filter(genres__id=int(genre_id))
                
            all_movies = list(movies_qs.order_by('display_order'))
            idx = all_movies.index(movie)
            
            if direction == 'up' and idx > 0:
                other = all_movies[idx - 1]
                movie.display_order, other.display_order = other.display_order, movie.display_order
                movie.save()
                other.save()
            elif direction == 'down' and idx < len(all_movies) - 1:
                other = all_movies[idx + 1]
                movie.display_order, other.display_order = other.display_order, movie.display_order
                movie.save()
                other.save()
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=400)


@login_required
def admin_edit_movie(request, movie_id):
    if not (request.user.is_staff or request.user.is_superuser or request.user.username == 'admin'):
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        try:
            movie.title = request.POST.get('title')
            movie.description = request.POST.get('description')
            movie.content_type = request.POST.get('content_type', 'movie')
            movie.poster_url = request.POST.get('poster_url')
            movie.banner_url = request.POST.get('banner_url')
            movie.video_url = request.POST.get('video_url', 'https://www.w3schools.com/html/mov_bbb.mp4')
            movie.rating = float(request.POST.get('rating', 0.0))
            movie.release_year = int(request.POST.get('release_year', 2024))
            movie.language = request.POST.get('language', 'English')
            movie.duration = request.POST.get('duration', '2h 15m')
            
            movie.is_trending = request.POST.get('is_trending') in ['true', 'on', '1', True]
            movie.is_popular = request.POST.get('is_popular') in ['true', 'on', '1', True]
            movie.is_latest = request.POST.get('is_latest') in ['true', 'on', '1', True]
            movie.is_top_rated = request.POST.get('is_top_rated') in ['true', 'on', '1', True]
            
            movie.cast = request.POST.get('cast', '')
            movie.crew = request.POST.get('crew', 'Director: John Doe')
            
            # Genres
            genre_ids = request.POST.getlist('genres')
            movie.genres.clear()
            if genre_ids:
                for gid in genre_ids:
                    try:
                        genre = Genre.objects.get(id=int(gid))
                        movie.genres.add(genre)
                    except (ValueError, Genre.DoesNotExist):
                        pass
                        
            # Optionally update display_order if provided
            display_order = request.POST.get('display_order')
            if display_order is not None:
                movie.display_order = int(display_order)
                
            movie.save()
            return redirect('admin_dashboard')
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f"Error editing title: {str(e)}"}, status=400)
            
            # Render dashboard with error message
            total_users = User.objects.count()
            total_movies = Movie.objects.count()
            revenue = 0
            for p in UserProfile.objects.all():
                if p.subscription_plan == 'Basic': revenue += 8.99
                elif p.subscription_plan == 'Standard': revenue += 13.99
                elif p.subscription_plan == 'Premium': revenue += 19.99
            users = User.objects.all().select_related('profile')
            movies = Movie.objects.all().order_by('display_order')
            genres = Genre.objects.all()
            return render(request, 'cine_verse/admin_dashboard.html', {
                'total_users': total_users,
                'total_movies': total_movies,
                'monthly_revenue': round(revenue, 2),
                'users': users,
                'movies': movies,
                'genres': genres,
                'error': f"Error editing title: {str(e)}"
            })
            
    return redirect('admin_dashboard')


def react_discover(request):
    movies = Movie.objects.all().order_by('display_order').prefetch_related('genres')
    genres = Genre.objects.all()
    
    watchlist_ids = set()
    if request.user.is_authenticated:
        watchlist_ids = set(request.user.profile.watchlist.values_list('id', flat=True))
    
    movies_list = []
    for m in movies:
        movies_list.append({
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'poster_url': m.poster_url,
            'rating': m.rating,
            'release_year': m.release_year,
            'duration': m.duration,
            'language': m.language,
            'genres': [g.slug for g in m.genres.all()],
            'in_watchlist': m.id in watchlist_ids,
            'content_type': m.content_type
        })
        
    genres_list = [{'name': g.name, 'slug': g.slug} for g in genres]
    
    context = {
        'movies_json': json.dumps(movies_list),
        'genres_json': json.dumps(genres_list),
    }
    return render(request, 'cine_verse/react_index.html', context)


# ──────────────────────────────────────────────
# Static Footer Pages
# ──────────────────────────────────────────────

def privacy_policy(request):
    sections = [
        {
            'icon': 'shield',
            'title': 'Information We Collect',
            'paragraphs': [
                'At CineVerse, we collect information that you provide directly to us when you create an account, update your profile, or interact with our platform.',
            ],
            'list_items': [
                'Account information (name, email, password)',
                'Profile preferences and favorite genres',
                'Watch history and viewing progress',
                'Device and browser information for analytics',
            ],
        },
        {
            'icon': 'visibility',
            'title': 'How We Use Your Information',
            'paragraphs': [
                'We use the information we collect to provide, maintain, and improve our streaming services, as well as to personalize your content recommendations.',
            ],
            'list_items': [
                'Delivering personalized movie and series recommendations',
                'Maintaining your watchlist and viewing history',
                'Improving the quality and performance of our platform',
                'Communicating with you about updates and new features',
            ],
        },
        {
            'icon': 'lock',
            'title': 'Data Protection',
            'paragraphs': [
                'We implement industry-standard security measures to protect your personal information. Your data is encrypted in transit and at rest. We never sell your personal data to third parties.',
                'You can request deletion of your account and all associated data at any time by contacting our support team.',
            ],
        },
        {
            'icon': 'share',
            'title': 'Third-Party Services',
            'paragraphs': [
                'We may share limited information with trusted third-party service providers who assist us in operating our platform, conducting our business, or serving our users. These parties agree to keep this information confidential.',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Privacy Policy',
        'sections': sections,
        'show_contact_cta': False,
    })


def terms_of_service(request):
    sections = [
        {
            'icon': 'gavel',
            'title': 'Acceptance of Terms',
            'paragraphs': [
                'By accessing and using CineVerse, you accept and agree to be bound by the terms and provisions of this agreement. If you do not agree to these terms, please do not use our services.',
            ],
        },
        {
            'icon': 'person',
            'title': 'User Accounts',
            'paragraphs': [
                'You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.',
            ],
            'list_items': [
                'You must be at least 13 years old to create an account',
                'You must provide accurate and complete registration information',
                'You are responsible for all activity on your account',
                'You must notify us immediately of any unauthorized use',
            ],
        },
        {
            'icon': 'movie',
            'title': 'Content & Licensing',
            'paragraphs': [
                'All content available on CineVerse, including but not limited to movies, series, images, and text, is protected by copyright and other intellectual property laws. You may not reproduce, distribute, or create derivative works from any content without explicit permission.',
            ],
        },
        {
            'icon': 'block',
            'title': 'Prohibited Activities',
            'paragraphs': [
                'When using CineVerse, you agree not to engage in any of the following prohibited activities:',
            ],
            'list_items': [
                'Sharing your account credentials with others',
                'Attempting to circumvent any content protection mechanisms',
                'Using automated tools to scrape or download content',
                'Uploading malicious code or interfering with the platform',
                'Violating any applicable laws or regulations',
            ],
        },
        {
            'icon': 'cancel',
            'title': 'Termination',
            'paragraphs': [
                'We reserve the right to terminate or suspend your account at any time, without prior notice, for conduct that we believe violates these Terms of Service or is harmful to other users, us, or third parties, or for any other reason at our sole discretion.',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Terms of Service',
        'sections': sections,
        'show_contact_cta': False,
    })


def cookie_preferences(request):
    sections = [
        {
            'icon': 'cookie',
            'title': 'What Are Cookies?',
            'paragraphs': [
                'Cookies are small text files that are stored on your device when you visit our website. They help us provide you with a better experience by remembering your preferences and understanding how you use our platform.',
            ],
        },
        {
            'icon': 'check_circle',
            'title': 'Essential Cookies',
            'paragraphs': [
                'These cookies are necessary for the website to function properly. They enable core features such as authentication, security, and session management. You cannot disable these cookies as the site will not work without them.',
            ],
            'list_items': [
                'Session management (keeping you logged in)',
                'CSRF protection for form submissions',
                'Security preferences and settings',
            ],
        },
        {
            'icon': 'analytics',
            'title': 'Analytics Cookies',
            'paragraphs': [
                'We use analytics cookies to understand how visitors interact with our platform. This helps us improve our services and provide better content recommendations. All analytics data is anonymized.',
            ],
            'list_items': [
                'Page visit frequency and duration',
                'Navigation patterns and popular content',
                'Device and browser type statistics',
            ],
        },
        {
            'icon': 'tune',
            'title': 'Preference Cookies',
            'paragraphs': [
                'These cookies remember your settings and preferences, such as your preferred genres, language selection, and display preferences. They enhance your personalized experience on CineVerse.',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Cookie Preferences',
        'sections': sections,
        'show_contact_cta': False,
    })


def help_center(request):
    sections = [
        {
            'icon': 'play_circle',
            'title': 'Getting Started',
            'paragraphs': [
                'Welcome to CineVerse! Here\'s how to get the most out of your streaming experience.',
            ],
            'list_items': [
                'Create an account or sign in to access all features',
                'Select your favorite genres to get personalized recommendations',
                'Browse movies and series from our curated collections',
                'Add titles to your watchlist to save them for later',
                'Track your viewing progress across all your devices',
            ],
        },
        {
            'icon': 'subscriptions',
            'title': 'Subscription & Billing',
            'paragraphs': [
                'CineVerse offers multiple subscription plans to suit your needs. Visit the Plans page to compare features and pricing.',
            ],
            'list_items': [
                'Free tier: Browse catalog and watch trailers',
                'Basic plan: Access to standard definition streaming',
                'Premium plan: Full HD streaming with unlimited devices',
                'You can upgrade, downgrade, or cancel your plan at any time',
            ],
        },
        {
            'icon': 'devices',
            'title': 'Supported Devices',
            'paragraphs': [
                'CineVerse works on all modern web browsers and devices. For the best experience, we recommend using the latest version of Chrome, Firefox, Safari, or Edge.',
            ],
        },
        {
            'icon': 'speed',
            'title': 'Streaming Quality',
            'paragraphs': [
                'Your streaming quality depends on your internet connection speed. We recommend a minimum of 5 Mbps for HD streaming and 25 Mbps for 4K content. The player will automatically adjust quality based on your connection.',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Help Center',
        'sections': sections,
        'show_contact_cta': True,
    })


def contact_us(request):
    sections = [
        {
            'icon': 'mail',
            'title': 'Email Support',
            'paragraphs': [
                'For general inquiries and support requests, reach out to us via email. Our team typically responds within 24 hours.',
                'Email: support@cineverse.com',
            ],
        },
        {
            'icon': 'schedule',
            'title': 'Support Hours',
            'paragraphs': [
                'Our customer support team is available to assist you during the following hours:',
            ],
            'list_items': [
                'Monday - Friday: 9:00 AM - 9:00 PM (IST)',
                'Saturday: 10:00 AM - 6:00 PM (IST)',
                'Sunday: 12:00 PM - 5:00 PM (IST)',
                'Holiday hours may vary — check our social media for updates',
            ],
        },
        {
            'icon': 'location_on',
            'title': 'Office Address',
            'paragraphs': [
                'CineVerse Global Headquarters',
                'Tech Park, Innovation Drive, Ahmedabad, Gujarat 380015, India',
            ],
        },
        {
            'icon': 'bug_report',
            'title': 'Report a Bug',
            'paragraphs': [
                'Found a bug or technical issue? Help us improve CineVerse by reporting it. Please include as much detail as possible — your browser, device, and steps to reproduce the issue.',
                'Bug reports: bugs@cineverse.com',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Contact Us',
        'sections': sections,
        'show_contact_cta': False,
    })


def faq(request):
    sections = [
        {
            'icon': 'help',
            'title': 'What is CineVerse?',
            'paragraphs': [
                'CineVerse is a next-generation movie and series streaming platform. It offers personalized recommendations, curated collections, and a seamless viewing experience across all your devices.',
            ],
        },
        {
            'icon': 'person_add',
            'title': 'How do I create an account?',
            'paragraphs': [
                'Click the "Sign In" button in the top navigation, then click "Register" to create a new account. You\'ll need to provide a username, email address, and password. After registration, you can customize your profile by selecting your favorite genres.',
            ],
        },
        {
            'icon': 'credit_card',
            'title': 'Is CineVerse free to use?',
            'paragraphs': [
                'CineVerse offers a free tier that allows you to browse the catalog and explore content. To stream full movies and series, you\'ll need to subscribe to one of our paid plans. Visit the Plans page to see pricing and features.',
            ],
        },
        {
            'icon': 'bookmark',
            'title': 'How does the watchlist work?',
            'paragraphs': [
                'You can add any movie or series to your watchlist by clicking the "+" button on any movie card. Your watchlist is accessible from the Dashboard (My List) section. You can also mark titles as favorites for quick access.',
            ],
        },
        {
            'icon': 'recommend',
            'title': 'How are recommendations generated?',
            'paragraphs': [
                'Our recommendation engine analyzes your favorite genres, watch history, and ratings to suggest content tailored to your taste. The more you watch and interact with the platform, the better our recommendations become.',
            ],
        },
        {
            'icon': 'security',
            'title': 'Is my data safe?',
            'paragraphs': [
                'Absolutely. We use industry-standard encryption and security practices to protect your personal information. We never sell your data to third parties. You can read more in our Privacy Policy page.',
            ],
        },
    ]
    return render(request, 'cine_verse/static_page.html', {
        'page_title': 'Frequently Asked Questions',
        'sections': sections,
        'show_contact_cta': True,
    })
