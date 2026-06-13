import { useState, useEffect } from 'react'

function Dashboard({ payload, user, csrfToken }) {
  const {
    watchlist = [],
    favorites = [],
    continue_watching = [],
    movies_watched_count = 0,
    time_watched_str = '',
    global_ranking = '',
    profile = {}
  } = payload;

  const [favoritesState, setFavoritesState] = useState(favorites);
  const [watchlistState, setWatchlistState] = useState(watchlist);
  const [continueWatchingState, setContinueWatchingState] = useState(continue_watching);

  useEffect(() => {
    if (!user) return;

    const fetchContinueWatching = () => {
      fetch('/api/watch/continue-watching/?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
          if (data.status === 'success') {
            setContinueWatchingState(data.continue_watching);
          }
        })
        .catch(err => console.error(err));
    };

    fetchContinueWatching();

    const handlePageShow = () => {
      fetchContinueWatching();
    };
    window.addEventListener('pageshow', handlePageShow);
    return () => {
      window.removeEventListener('pageshow', handlePageShow);
    };
  }, [user]);

  const handleCardClick = (id) => {
    window.location.href = `/movies/${id}/`;
  };

  const [draggedItem, setDraggedItem] = useState(null);
  const [draggedIndex, setDraggedIndex] = useState(null);
  const [draggedSection, setDraggedSection] = useState(null); // 'favorites' or 'watchlist'

  const saveOrder = (type, items) => {
    const movieIds = items.map(m => m.id);
    fetch('/api/profile/reorder/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        type: type,
        movie_ids: movieIds
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status !== 'success') {
        console.error('Error saving reorder:', data.message);
      }
    })
    .catch(err => console.error(err));
  };

  // Drag and Drop Handlers
  const handleDragStart = (e, index, section, item) => {
    setDraggedItem(item);
    setDraggedIndex(index);
    setDraggedSection(section);
    e.dataTransfer.effectAllowed = 'move';
    e.currentTarget.classList.add('opacity-50');
  };

  const handleDragEnd = (e) => {
    e.currentTarget.classList.remove('opacity-50');
    setDraggedItem(null);
    setDraggedIndex(null);
    setDraggedSection(null);
  };

  const handleDragOver = (e, index, section) => {
    e.preventDefault();
    if (section !== draggedSection || index === draggedIndex) return;

    const list = section === 'favorites' ? [...favoritesState] : [...watchlistState];
    const itemToMove = list[draggedIndex];
    
    // Perform reorder in place
    list.splice(draggedIndex, 1);
    list.splice(index, 0, itemToMove);

    setDraggedIndex(index);
    if (section === 'favorites') {
      setFavoritesState(list);
    } else {
      setWatchlistState(list);
    }
  };

  const handleDrop = (section) => {
    const list = section === 'favorites' ? favoritesState : watchlistState;
    saveOrder(section, list);
  };

  // Responsive button-based sorting helpers (highly convenient for touch screens!)
  const moveItem = (section, index, direction) => {
    const list = section === 'favorites' ? [...favoritesState] : [...watchlistState];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;
    
    if (targetIndex < 0 || targetIndex >= list.length) return;

    const temp = list[index];
    list[index] = list[targetIndex];
    list[targetIndex] = temp;

    if (section === 'favorites') {
      setFavoritesState(list);
    } else {
      setWatchlistState(list);
    }
    saveOrder(section, list);
  };

  return (
    <main className="pt-44 md:pt-28 pb-section-gap px-gutter max-w-[1440px] mx-auto text-left select-none">
      {/* Profile Overview Widgets */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-gutter mb-section-gap">
        <div className="lg:col-span-8 flex flex-col justify-center">
          <h1 className="font-headline-lg text-3xl sm:text-headline-lg text-white mb-2 leading-tight">
            Welcome back, {user}!
          </h1>
          <p className="text-on-surface-variant font-body-lg text-body-lg max-w-2xl">
            Your personalized cinematic journey continues. We've curated a list of premieres and recommendations based on your love for{' '}
            <span className="text-primary-container font-bold">
              {profile.favorite_genres?.length > 0 ? profile.favorite_genres.join(', ') : 'adding genres in settings'}
            </span>.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <div className="glass-panel px-6 py-4 rounded-xl flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-primary-container/20 flex items-center justify-center">
                <span className="material-symbols-outlined text-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>workspace_premium</span>
              </div>
              <div>
                <p className="text-on-surface-variant text-label-caps font-label-caps">ACTIVE PLAN</p>
                <p className="text-on-surface font-bold text-white">{profile.subscription_plan} Plan</p>
              </div>
            </div>
            <div className="glass-panel px-6 py-4 rounded-xl flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-secondary-container/20 flex items-center justify-center">
                <span className="material-symbols-outlined text-secondary" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
              </div>
              <div>
                <p className="text-on-surface-variant text-label-caps font-label-caps">FAVORITE GENRES</p>
                <p className="text-on-surface font-bold text-white truncate max-w-[180px]" title={profile.favorite_genres?.join(', ')}>
                  {profile.favorite_genres?.length > 0 ? profile.favorite_genres.join(', ') : 'Not Set'}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Account Summary Sidebar Widget */}
        <div className="lg:col-span-4">
          <div className="glass-panel p-6 rounded-xl relative overflow-hidden h-full">
            <div className="absolute -right-4 -top-4 w-32 h-32 bg-primary-container/10 blur-[60px] rounded-full"></div>
            <div className="relative z-10 flex flex-col h-full justify-between">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-headline-md font-headline-md text-white">Profile Summary</h3>
                <a href="/profile/" className="text-primary-container hover:underline text-sm font-bold">Edit</a>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Movies Watched</span>
                  <span className="text-white font-bold">{movies_watched_count}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Time Watched</span>
                  <span className="text-white font-bold">{time_watched_str}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/60">Global Ranking</span>
                  <span className="text-white font-bold">{global_ranking}</span>
                </div>
              </div>
              <div className="mt-8 pt-6 border-t border-white/5">
                <a href="/profile/" className="block w-full py-3 bg-primary-container text-on-primary-container rounded-lg font-bold text-center hover:brightness-110 transition-all">Account Settings</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Recently Watched */}
      <section className="mb-section-gap">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-headline-md font-headline-md text-white">Recently Watched</h2>
          <a className="text-primary-container flex items-center gap-2 font-bold hover:gap-3 transition-all" href="/">
            Watch More <span className="material-symbols-outlined text-sm">arrow_forward</span>
          </a>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {continueWatchingState.map(item => (
            <div 
              key={item.movie.id}
              onClick={() => window.location.href = `/movies/${item.movie.id}/watch/`}
              className="group relative aspect-video bg-surface-container-high rounded-xl overflow-hidden cursor-pointer movie-card ring-1 ring-white/10"
            >
              <img 
                alt={item.movie.title} 
                className="w-full h-full object-cover" 
                src={item.movie.banner_url || item.movie.poster_url} 
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'https://placehold.co/320x180?text=No+Preview';
                }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0F1117] via-transparent to-transparent opacity-60"></div>
              <div className="absolute bottom-0 left-0 w-full px-4 pb-4">
                <p className="font-bold truncate text-white">{item.movie.title}</p>
              </div>
              <div className="overlay absolute inset-0 bg-black/40 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button className="w-12 h-12 rounded-full bg-primary-container flex items-center justify-center text-white scale-90 hover:scale-110 transition-transform shadow-lg cursor-pointer">
                  <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
                </button>
              </div>
            </div>
          ))}
          {continueWatchingState.length === 0 && (
            <div className="col-span-full p-8 glass-panel text-center rounded-xl">
              <p className="text-on-surface-variant text-sm">You haven't watched any movies yet. Explore titles to begin!</p>
            </div>
          )}
        </div>
      </section>

      {/* Favorites & Watchlist Reordering */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
        {/* Favorites Grid */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-headline-md font-headline-md text-white flex items-center gap-2">
              Your Favorites
              <span className="text-xs font-normal text-white/40 tracking-normal hidden md:inline">(Drag to reorder)</span>
            </h2>
            <span className="material-symbols-outlined text-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
          </div>

          <div 
            className="grid grid-cols-2 sm:grid-cols-3 gap-4" 
            id="favorites-grid"
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => handleDrop('favorites')}
          >
            {favoritesState.map((movie, index) => (
              <div
                key={movie.id}
                draggable
                onDragStart={(e) => handleDragStart(e, index, 'favorites', movie)}
                onDragEnd={handleDragEnd}
                onDragOver={(e) => handleDragOver(e, index, 'favorites')}
                onClick={() => handleCardClick(movie.id)}
                className="clickable-card aspect-[2/3] bg-surface-container rounded-lg overflow-hidden group cursor-grab active:cursor-grabbing movie-card relative ring-1 ring-white/10"
              >
                <img 
                  alt={movie.title} 
                  className="w-full h-full object-cover pointer-events-none" 
                  src={movie.poster_url} 
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = `https://placehold.co/150x225?text=${encodeURIComponent(movie.title)}`;
                  }}
                />
                
                {/* Mobile reorder buttons */}
                <div className="absolute top-2 right-2 flex gap-1 z-20 sm:hidden">
                  {index > 0 && (
                    <button
                      onClick={(e) => { e.stopPropagation(); moveItem('favorites', index, 'up'); }}
                      className="w-6 h-6 rounded-md bg-black/70 hover:bg-black text-white flex items-center justify-center cursor-pointer"
                    >
                      <span className="material-symbols-outlined text-sm">arrow_back</span>
                    </button>
                  )}
                  {index < favoritesState.length - 1 && (
                    <button
                      onClick={(e) => { e.stopPropagation(); moveItem('favorites', index, 'down'); }}
                      className="w-6 h-6 rounded-md bg-black/70 hover:bg-black text-white flex items-center justify-center cursor-pointer"
                    >
                      <span className="material-symbols-outlined text-sm">arrow_forward</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
            {favoritesState.length === 0 && (
              <div className="col-span-full p-8 glass-panel text-center rounded-xl">
                <p className="text-on-surface-variant text-sm">No favorites added yet.</p>
              </div>
            )}
          </div>
        </div>

        {/* Watchlist Vertical List */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-headline-md font-headline-md text-white flex items-center gap-2">
              My Watchlist
              <span className="text-xs font-normal text-white/40 tracking-normal hidden md:inline">(Drag to reorder)</span>
            </h2>
            <span className="material-symbols-outlined text-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>bookmark</span>
          </div>

          <div 
            className="space-y-4" 
            id="watchlist-list"
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => handleDrop('watchlist')}
          >
            {watchlistState.map((movie, index) => (
              <div
                key={movie.id}
                draggable
                onDragStart={(e) => handleDragStart(e, index, 'watchlist', movie)}
                onDragEnd={handleDragEnd}
                onDragOver={(e) => handleDragOver(e, index, 'watchlist')}
                onClick={() => handleCardClick(movie.id)}
                className="clickable-card glass-panel p-4 rounded-xl flex items-center gap-4 group hover:bg-white/5 cursor-grab active:cursor-grabbing transition-all duration-300 relative border border-white/5"
              >
                <div className="w-20 h-12 bg-surface-container rounded overflow-hidden flex-shrink-0 pointer-events-none">
                  <img 
                    alt={movie.title} 
                    className="w-full h-full object-cover" 
                    src={movie.banner_url || movie.poster_url} 
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = 'https://placehold.co/100x60?text=Movie';
                    }}
                  />
                </div>
                <div className="flex-grow text-left pointer-events-none">
                  <h4 className="font-bold text-white truncate">{movie.title}</h4>
                  <p className="text-xs text-on-surface-variant">{movie.release_year} • {movie.duration}</p>
                </div>
                
                {/* Mobile/Touch sorting triggers */}
                <div className="flex items-center gap-2 z-20">
                  <div className="flex flex-col gap-1 sm:hidden">
                    {index > 0 && (
                      <button
                        onClick={(e) => { e.stopPropagation(); moveItem('watchlist', index, 'up'); }}
                        className="w-6 h-6 rounded bg-black/40 hover:bg-black/60 text-white flex items-center justify-center cursor-pointer"
                      >
                        <span className="material-symbols-outlined text-sm">keyboard_arrow_up</span>
                      </button>
                    )}
                    {index < watchlistState.length - 1 && (
                      <button
                        onClick={(e) => { e.stopPropagation(); moveItem('watchlist', index, 'down'); }}
                        className="w-6 h-6 rounded bg-black/40 hover:bg-black/60 text-white flex items-center justify-center cursor-pointer"
                      >
                        <span className="material-symbols-outlined text-sm">keyboard_arrow_down</span>
                      </button>
                    )}
                  </div>
                  
                  <button 
                    onClick={(e) => { e.stopPropagation(); window.location.href = `/movies/${movie.id}/watch/`; }}
                    className="play-btn w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-on-surface-variant hover:text-primary-container hover:border-primary-container transition-all bg-transparent cursor-pointer"
                  >
                    <span className="material-symbols-outlined text-sm">play_arrow</span>
                  </button>
                </div>
              </div>
            ))}
            {watchlistState.length === 0 && (
              <div className="p-8 glass-panel text-center rounded-xl">
                <p className="text-on-surface-variant text-sm">Your watchlist is currently empty.</p>
              </div>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}

export default Dashboard;
