import { useState, useMemo, useEffect } from 'react'

function Explore({ payload, user, csrfToken, page }) {
  const {
    all_movies = [],
    genres = [],
    languages = [],
    years = [],
    selected_genre = '',
    selected_language = '',
    selected_rating = '0',
    selected_year = '',
    search_query = '',
    selected_content_type = 'all',
    selected_sort = 'popularity',
    trending_searches = [],
    total_count = 0,
    movie_count = 0,
    tv_count = 0
  } = payload;

  const isSearchPage = page === 'search_results';

  // React state initialized from Django server context
  const [searchQuery, setSearchQuery] = useState(search_query);
  const [contentType, setContentType] = useState(selected_content_type); // 'all', 'movie', 'series'
  const [selectedGenre, setSelectedGenre] = useState(selected_genre);
  const [minRating, setMinRating] = useState(parseFloat(selected_rating || '0'));
  const [selectedLanguage, setSelectedLanguage] = useState(selected_language);
  const [selectedYear, setSelectedYear] = useState(selected_year);
  const [sortBy, setSortBy] = useState(selected_sort);
  
  const [movies, setMovies] = useState(all_movies);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15;

  // Watchlist POST toggle handler
  const toggleWatchlist = (e, movieId) => {
    e.stopPropagation();
    e.preventDefault();
    if (!user) {
      window.location.href = '/login/';
      return;
    }

    fetch(`/api/movies/${movieId}/watchlist/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        setMovies(prev => prev.map(m => m.id === movieId ? { ...m, in_watchlist: data.added } : m));
      }
    })
    .catch(err => console.error(err));
  };

  const handleCardClick = (movieId) => {
    window.location.href = `/movies/${movieId}/`;
  };

  const handlePlayClick = (e, movieId) => {
    e.stopPropagation();
    e.preventDefault();
    window.location.href = `/movies/${movieId}/watch/`;
  };

  // Client-side processed movies list
  const processedMovies = useMemo(() => {
    let result = [...movies];

    // Search query filter (only filter if search page has query, or on regular catalog explore)
    if (isSearchPage) {
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        result = result.filter(m => 
          m.title.toLowerCase().includes(query) || 
          (m.description && m.description.toLowerCase().includes(query))
        );
      } else {
        // If search page is empty, display empty grid (will show trending searches separately)
        return [];
      }
    } else {
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        result = result.filter(m => 
          m.title.toLowerCase().includes(query) || 
          (m.description && m.description.toLowerCase().includes(query))
        );
      }
    }

    // Content type filter
    if (contentType !== 'all') {
      result = result.filter(m => m.content_type === contentType);
    }

    // Genre filter
    if (selectedGenre) {
      result = result.filter(m => m.genres && m.genres.includes(selectedGenre));
    }

    // Minimum rating filter
    if (minRating > 0) {
      result = result.filter(m => m.rating >= minRating);
    }

    // Language filter
    if (selectedLanguage) {
      result = result.filter(m => m.language === selectedLanguage);
    }

    // Release year filter
    if (selectedYear) {
      result = result.filter(m => m.release_year === parseInt(selectedYear, 10));
    }

    // Sort order
    if (sortBy === 'latest') {
      result.sort((a, b) => b.release_year - a.release_year);
    } else if (sortBy === 'rating') {
      result.sort((a, b) => b.rating - a.rating);
    } else {
      // 'popularity': display order sorted by original display_order
      result.sort((a, b) => a.display_order - b.display_order);
    }

    setCurrentPage(1);
    return result;
  }, [movies, searchQuery, contentType, selectedGenre, minRating, selectedLanguage, selectedYear, sortBy, isSearchPage]);

  // Paginated chunk
  const paginatedMovies = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return processedMovies.slice(startIndex, startIndex + itemsPerPage);
  }, [processedMovies, currentPage]);

  const totalPages = Math.ceil(processedMovies.length / itemsPerPage);

  return (
    <main className="pt-44 md:pt-28 pb-section-gap max-w-[1440px] mx-auto px-gutter min-h-screen">
      {/* Header Titles & Subtitles */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8 text-left">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-white">
            {isSearchPage 
              ? `Search Results` 
              : (contentType === 'series' ? 'Explore Series' : (contentType === 'movie' ? 'Explore Movies' : 'Explore Movies & Series'))
            }
          </h1>
          <p className="text-on-surface-variant font-body-md max-w-xl mt-1">
            {isSearchPage
              ? (searchQuery ? `Showing matches for "${searchQuery}"` : 'Enter a query in the search bar above to begin.')
              : (contentType === 'series' ? 'Browse the full series catalog without movie results mixed in.' : (contentType === 'movie' ? 'Browse only films, with every result tied to the movie catalog.' : 'Curated selection of global cinema and series, from pulse-pounding action to heart-wrenching dramas.'))
            }
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="glass-panel p-2 rounded-xl flex items-center gap-2">
            <button
              onClick={() => setContentType('all')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${contentType === 'all' ? 'bg-primary-container text-white' : 'text-on-surface-variant hover:bg-white/10 hover:text-white'}`}
            >
              All
            </button>
            <button
              onClick={() => setContentType('movie')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${contentType === 'movie' ? 'bg-primary-container text-white' : 'text-on-surface-variant hover:bg-white/10 hover:text-white'}`}
            >
              Movies
            </button>
            <button
              onClick={() => setContentType('series')}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${contentType === 'series' ? 'bg-primary-container text-white' : 'text-on-surface-variant hover:bg-white/10 hover:text-white'}`}
            >
              Series
            </button>
          </div>

          <button
            onClick={() => setMobileFilterOpen(!mobileFilterOpen)}
            className="lg:hidden flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold bg-white/5 border border-white/10 text-white hover:bg-white/10 transition-colors"
          >
            <span className="material-symbols-outlined text-lg">filter_list</span>
            <span>Filters</span>
          </button>

          {!isSearchPage && (
            <>
              <span className="text-label-caps font-label-caps px-2 opacity-50 uppercase text-white">Sort By:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-transparent border-none focus:ring-0 text-body-md font-medium text-primary cursor-pointer pr-8 focus:outline-none"
              >
                <option value="popularity" className="bg-[#1A1D29] text-white">Popularity</option>
                <option value="latest" className="bg-[#1A1D29] text-white">Latest Release</option>
                <option value="rating" className="bg-[#1A1D29] text-white">Highest Rating</option>
              </select>
            </>
          )}
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar Filters */}
        <aside className={`${mobileFilterOpen ? 'block' : 'hidden'} lg:block lg:w-64 space-y-8 flex-shrink-0 w-full text-left`}>
          {/* Quick search input inside sidebar for live explore */}
          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="font-headline-md text-body-lg mb-4 flex items-center gap-2 text-white">
              <span className="material-symbols-outlined text-primary-container">search</span>
              Search
            </h3>
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search..."
                className="w-full bg-[#1A1D29] border border-white/10 rounded-lg py-2.5 px-4 text-xs focus:border-primary-container focus:outline-none text-white placeholder-white/30"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-2.5 text-white/50 hover:text-white"
                >
                  <span className="material-symbols-outlined text-sm">close</span>
                </button>
              )}
            </div>
          </div>

          {/* Genre Badges */}
          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="font-headline-md text-body-lg mb-4 flex items-center gap-2 text-white">
              <span className="material-symbols-outlined text-primary-container">filter_list</span>
              Genres
            </h3>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedGenre('')}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${!selectedGenre ? 'bg-primary-container text-white animate-pulse' : 'bg-surface-variant text-on-surface-variant hover:bg-surface-container-high'}`}
              >
                All
              </button>
              {genres.map(g => (
                <button
                  key={g.slug}
                  onClick={() => setSelectedGenre(g.slug)}
                  className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${selectedGenre === g.slug ? 'bg-primary-container text-white' : 'bg-surface-variant text-on-surface-variant hover:bg-surface-container-high'}`}
                >
                  {g.name}
                </button>
              ))}
            </div>
          </div>

          {/* Ratings, Languages, Years slider grids */}
          <div className="glass-panel p-6 rounded-2xl space-y-6">
            <div>
              <h3 className="text-xs font-bold tracking-widest text-on-surface-variant mb-3 uppercase">
                MINIMUM RATING: <span className="text-primary-container">{minRating}</span>
              </h3>
              <input
                type="range"
                min="0"
                max="10"
                step="0.5"
                value={minRating}
                onChange={(e) => setMinRating(parseFloat(e.target.value))}
                className="w-full accent-primary-container h-1 bg-surface-variant rounded-full appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs mt-2 opacity-60 text-on-surface-variant">
                <span>0</span>
                <span>5</span>
                <span>10</span>
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold tracking-widest text-on-surface-variant mb-3 uppercase">LANGUAGE</h3>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full bg-[#1A1D29] border border-white/10 rounded-lg py-2 px-3 text-body-md focus:border-primary-container focus:outline-none text-white cursor-pointer"
              >
                <option value="">All Languages</option>
                {languages.map(lang => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            <div>
              <h3 className="text-xs font-bold tracking-widest text-on-surface-variant mb-3 uppercase">RELEASE YEAR</h3>
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
                className="w-full bg-[#1A1D29] border border-white/10 rounded-lg py-2 px-3 text-body-md focus:border-primary-container focus:outline-none text-white cursor-pointer"
              >
                <option value="">All Years</option>
                {years.map(yr => (
                  <option key={yr} value={yr}>{yr}</option>
                ))}
              </select>
            </div>

            {(searchQuery || selectedGenre || minRating > 0 || selectedLanguage || selectedYear || contentType !== 'all') && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setContentType('all');
                  setSelectedGenre('');
                  setMinRating(0);
                  setSelectedLanguage('');
                  setSelectedYear('');
                  setSortBy('popularity');
                }}
                className="w-full py-2 bg-white/5 border border-white/10 text-white text-xs font-bold rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
              >
                Reset Filters
              </button>
            )}
          </div>
        </aside>

        {/* Catalog Results Grid */}
        <div className="flex-grow">
          {processedMovies.length === 0 ? (
            <div className="p-12 glass-panel text-center rounded-xl flex flex-col items-center justify-center">
              <p className="text-on-surface-variant text-sm mb-6">No movies match your filter settings.</p>
              {isSearchPage && trending_searches.length > 0 && (
                <div className="w-full max-w-lg mt-4 text-center">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-white/50 mb-3">Trending Searches</h4>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {trending_searches.map(trend => (
                      <button
                        key={trend.id}
                        onClick={() => setSearchQuery(trend.title)}
                        className="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-white text-xs font-bold hover:bg-white/10 transition-all cursor-pointer"
                      >
                        {trend.title}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-gutter">
                {paginatedMovies.map(movie => {
                  const mState = movies.find(m => m.id === movie.id) || movie;
                  return (
                    <div
                      key={movie.id}
                      onClick={() => handleCardClick(movie.id)}
                      className="movie-card relative aspect-[2/3] overflow-hidden rounded-2xl bg-black/80 cursor-pointer group shadow-xl shadow-black/25 ring-1 ring-white/10 animate-fade-in"
                    >
                      <img
                        className="absolute inset-0 w-full h-full object-contain object-center bg-black/80 transition-transform duration-500 group-hover:scale-[1.02]"
                        src={movie.poster_url}
                        alt={`${movie.title} poster`}
                        loading="lazy"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = `https://placehold.co/300x450?text=${encodeURIComponent(movie.title)}`;
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/35 to-transparent opacity-90"></div>
                      
                      {/* Overlay card quick info */}
                      <div className="quick-info absolute inset-0 opacity-100 translate-y-0 sm:opacity-0 sm:translate-y-4 sm:group-hover:opacity-100 sm:group-hover:translate-y-0 transition-all duration-300 flex flex-col justify-end p-4 sm:p-5">
                        <div className="space-y-3">
                          <div className="flex gap-2">
                            <button
                              type="button"
                              onClick={(e) => handlePlayClick(e, movie.id)}
                              className="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center text-white cursor-pointer hover:scale-105 transition-transform"
                            >
                              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
                                play_arrow
                              </span>
                            </button>
                            
                            <button
                              type="button"
                              onClick={(e) => toggleWatchlist(e, movie.id)}
                              className={`w-10 h-10 rounded-full glass-panel flex items-center justify-center text-white hover:bg-white hover:text-black transition-colors cursor-pointer ${
                                mState.in_watchlist ? 'bg-primary-container' : ''
                              }`}
                            >
                              <span className="material-symbols-outlined">
                                {mState.in_watchlist ? 'check' : 'add'}
                              </span>
                            </button>
                          </div>
                          
                          <div className="text-left">
                            <h4 className="font-headline-md text-body-lg leading-tight text-white line-clamp-2">
                              {movie.title}
                            </h4>
                            <div className="flex items-center gap-2 text-label-caps text-white/80 mt-1 flex-wrap">
                              <span className="flex items-center text-primary">
                                <span className="material-symbols-outlined text-[14px] mr-1" style={{ fontVariationSettings: "'FILL' 1" }}>
                                  star
                                </span>
                                {movie.rating}
                              </span>
                              <span>•</span>
                              <span>{movie.release_year}</span>
                              <span>•</span>
                              <span>{movie.duration}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>

              {/* Grid Pagination footer */}
              {totalPages > 1 && (
                <div className="mt-12 flex justify-center items-center gap-2">
                  <button
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className={`w-10 h-10 rounded-lg glass-panel flex items-center justify-center transition-colors ${currentPage === 1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-white hover:text-black cursor-pointer'}`}
                  >
                    <span className="material-symbols-outlined">chevron_left</span>
                  </button>
                  
                  {Array.from({ length: totalPages }).map((_, idx) => {
                    const pageNum = idx + 1;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold transition-all cursor-pointer ${currentPage === pageNum ? 'bg-primary-container text-white' : 'glass-panel hover:bg-white hover:text-black'}`}
                      >
                        {pageNum}
                      </button>
                    )
                  })}
                  
                  <button
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className={`w-10 h-10 rounded-lg glass-panel flex items-center justify-center transition-colors ${currentPage === totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-white hover:text-black cursor-pointer'}`}
                  >
                    <span className="material-symbols-outlined">chevron_right</span>
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  )
}

export default Explore;
