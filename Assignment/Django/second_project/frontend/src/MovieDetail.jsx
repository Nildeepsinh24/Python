import { useState } from 'react'

function MovieDetail({ payload, user, csrfToken }) {
  const {
    movie,
    similar_movies = [],
    in_watchlist: initialInWatchlist,
    in_favorites: initialInFavorites,
    cast_list = [],
    crew_list = [],
    parts = [],
    parent_movie = null
  } = payload;

  const [inWatchlist, setInWatchlist] = useState(initialInWatchlist);
  const [inFavorites, setInFavorites] = useState(initialInFavorites);

  const playableMovieId = (parts.length > 0 && (movie.content_type === 'series' ? !movie.parent_id : parts.some(p => p.id === movie.id) && movie.id === parent_movie?.id)) ? parts[0].id : movie.id;

  // Compute release year text (range for parent collections/series, or single year for parts)
  let releaseYearText = String(movie.release_year);
  if (!movie.parent_id && parts.length > 0) {
    const years = [movie.release_year, ...parts.map(p => p.release_year)].filter(Boolean);
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    if (minYear !== maxYear) {
      releaseYearText = `${minYear} - ${maxYear}`;
    }
  }

  const toggleWatchlist = () => {
    if (!user) {
      window.location.href = '/login/';
      return;
    }

    fetch(`/api/movies/${movie.id}/watchlist/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        setInWatchlist(data.added);
      }
    })
    .catch(err => console.error(err));
  };

  const toggleFavorite = () => {
    if (!user) {
      window.location.href = '/login/';
      return;
    }

    fetch(`/api/movies/${movie.id}/favorite/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        setInFavorites(data.added);
      }
    })
    .catch(err => console.error(err));
  };

  const handleCardClick = (id) => {
    window.location.href = `/movies/${id}/`;
  };

  return (
    <div className="relative pt-44 md:pt-28 pb-section-gap max-w-[1440px] mx-auto px-gutter min-h-screen text-left">
      {/* Blurred Backdrop Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-25 filter blur-3xl pointer-events-none z-0"
        style={{ backgroundImage: `url('${movie.banner_url || movie.poster_url}')` }}
      ></div>

      <div className="relative z-10">
        {/* Main Columns */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-12 mb-16">
          {/* Left Column: Poster Image */}
          <div className="md:col-span-4 lg:col-span-3 flex justify-center md:justify-start lg:justify-start">
            <div className="w-64 lg:w-full aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl shadow-black/60 border border-white/10 bg-black/40">
              <img 
                src={movie.poster_url} 
                alt={`${movie.title} poster`} 
                className="w-full h-full object-cover object-center"
              />
            </div>
          </div>

          {/* Center Column: Title & Overview */}
          <div className="md:col-span-8 lg:col-span-6 flex flex-col justify-center">
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <span className="bg-primary-container text-white text-[10px] font-bold px-2.5 py-0.5 rounded tracking-widest uppercase">
                {movie.content_type === 'series' ? 'TV Series' : 'Movie'}
              </span>
              <span className="text-white/60 font-body-md text-sm">{releaseYearText}</span>
              <span className="text-white/60 font-body-md text-sm border border-white/20 px-1.5 rounded">{movie.language}</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-extrabold text-white leading-tight uppercase mb-6 tracking-tight">
              {movie.title}
            </h1>

            {/* Quick Action buttons */}
            <div className="flex flex-wrap gap-4 mb-8">
              <a 
                href={`/movies/${playableMovieId}/watch/`} 
                className="px-8 py-3.5 bg-primary-container text-on-primary-container font-bold rounded-xl hover:brightness-110 transition-all flex items-center gap-2 shadow-lg shadow-primary-container/20"
              >
                <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
                <span>Play Now</span>
              </a>
              
              <button 
                onClick={toggleWatchlist}
                className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all cursor-pointer border ${
                  inWatchlist 
                    ? 'bg-primary-container text-white border-primary-container' 
                    : 'bg-white/5 border-white/10 text-white hover:bg-white/10'
                }`}
                title="Add to Watchlist"
              >
                <span className="material-symbols-outlined">{inWatchlist ? 'check' : 'add'}</span>
              </button>

              <button 
                onClick={toggleFavorite}
                className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all cursor-pointer border ${
                  inFavorites 
                    ? 'bg-red-600 text-white border-red-600' 
                    : 'bg-white/5 border-white/10 text-white hover:bg-white/10'
                }`}
                title="Add to Favorites"
              >
                <span className="material-symbols-outlined" style={{ fontVariationSettings: inFavorites ? "'FILL' 1" : "'FILL' 0" }}>
                  favorite
                </span>
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="text-xs font-bold tracking-widest text-white/40 uppercase mb-2">Overview</h3>
                <p className="text-white/80 text-body-lg leading-relaxed">{movie.description}</p>
              </div>

              {cast_list.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold tracking-widest text-white/40 uppercase mb-2">Cast</h3>
                  <div className="flex flex-wrap gap-2">
                    {cast_list.map((actor, idx) => (
                      <span key={idx} className="bg-white/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-white/80 border border-white/5">
                        {actor}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {crew_list.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold tracking-widest text-white/40 uppercase mb-2">Crew</h3>
                  <div className="flex flex-wrap gap-2">
                    {crew_list.map((member, idx) => (
                      <span key={idx} className="bg-white/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-white/80 border border-white/5">
                        {member}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* TV Seasons or Movie Collection Section */}
              {parts.length > 0 && (
                <div className="border-t border-white/5 pt-6 mt-6">
                  <h3 className="text-xs font-bold tracking-widest text-white/40 uppercase mb-4">
                    {movie.content_type === 'series' ? 'Seasons' : 'Movies in this Collection'}
                  </h3>
                  <div className="flex flex-row gap-6 overflow-x-auto pb-4 custom-scrollbar scroll-smooth">
                    {parts.map(part => {
                      const isActive = part.id === movie.id;
                      return (
                        <div 
                          key={part.id}
                          onClick={() => window.location.href = `/movies/${part.id}/`}
                          className={`w-72 sm:w-80 flex-shrink-0 flex flex-col rounded-2xl border transition-all duration-300 cursor-pointer group bg-white/5 ${
                            isActive 
                              ? 'border-primary-container ring-2 ring-primary-container/30 shadow-lg shadow-primary-container/10' 
                              : 'border-white/10 hover:bg-white/10 hover:border-white/20'
                          }`}
                        >
                          <div className="relative w-full aspect-video rounded-t-xl overflow-hidden bg-black/40">
                            <img 
                              src={part.banner_url || part.poster_url} 
                              alt={part.title}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                            />
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                              <span className="material-symbols-outlined text-4xl text-white">play_circle</span>
                            </div>
                            <div className="absolute top-2 left-2 bg-black/60 px-2 py-0.5 rounded text-[10px] font-bold text-white tracking-wide uppercase">
                              {part.part_name || (movie.content_type === 'series' ? `Season ${part.part_number}` : `Part ${part.part_number}`)}
                            </div>
                          </div>
                          <div className="p-4 flex flex-col justify-between flex-grow text-left">
                            <div>
                              <div className="flex items-center justify-between gap-2 mb-1">
                                <h4 className={`font-bold text-sm sm:text-base truncate flex-grow ${isActive ? 'text-primary-container' : 'text-white group-hover:text-primary-container transition-colors'}`}>
                                  {part.title}
                                </h4>
                                {part.rating > 0 && (
                                  <span className="text-[10px] bg-white/5 border border-white/10 px-1.5 py-0.5 rounded text-amber-400 flex items-center font-bold flex-shrink-0">
                                    <span className="material-symbols-outlined text-[10px] mr-0.5" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                                    {part.rating}
                                  </span>
                                )}
                              </div>
                              <p className="text-[11px] text-white/50 mb-2 font-medium">{part.release_year} • {part.duration}</p>
                              <p className="text-xs text-white/70 line-clamp-2 leading-relaxed">{part.description}</p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Metadata Card */}
          <div className="md:col-span-12 lg:col-span-3">
            <div className="glass-panel p-6 rounded-2xl relative overflow-hidden">
              <h3 className="font-headline-md text-body-lg mb-6 text-white">Details</h3>
              <div className="space-y-4 text-sm">
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-white/50">Rating</span>
                  <span className="font-bold text-primary flex items-center">
                    <span className="material-symbols-outlined text-sm mr-1" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                    {movie.rating} / 10
                  </span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-white/50">Release Year</span>
                  <span className="font-bold text-white">{releaseYearText}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-white/50">Duration</span>
                  <span className="font-bold text-white">{movie.duration}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-white/50">Language</span>
                  <span className="font-bold text-white">{movie.language}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Similar Movies Section */}
        {similar_movies.length > 0 && (
          <section className="border-t border-white/5 pt-12">
            <h2 className="font-headline-md text-headline-md mb-8 text-white">More Like This</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 sm:gap-6">
              {similar_movies.map(rel => (
                <div 
                  key={rel.id} 
                  onClick={() => handleCardClick(rel.id)}
                  className="movie-card relative aspect-[2/3] rounded-xl overflow-hidden glass-panel cursor-pointer group ring-1 ring-white/10"
                >
                  <img 
                    alt={rel.title} 
                    className="w-full h-full object-cover" 
                    src={rel.poster_url} 
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-3 text-left">
                    <p className="font-bold text-sm leading-tight text-white truncate mb-1">{rel.title}</p>
                    <p className="text-[10px] text-white/60">{rel.release_year}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default MovieDetail;
