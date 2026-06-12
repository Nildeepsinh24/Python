import { useState, useEffect } from 'react'

function Home({ payload, user, csrfToken }) {
  const {
    featured_movie,
    trending_movies = [],
    popular_movies = [],
    latest_movies = [],
    top_rated_movies = [],
    continue_watching = [],
    recommended_movies = [],
    show_genre_modal: initialShowGenreModal,
    all_genres = [],
    all_movies = []
  } = payload;

  const [moviesState, setMoviesState] = useState(all_movies);
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [showModal, setShowModal] = useState(initialShowGenreModal);
  const [selectedModalGenres, setSelectedModalGenres] = useState([]);
  const [modalError, setModalError] = useState('');

  // Synchronize dynamic watchlist actions in Home components
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
        setMoviesState(prev => prev.map(m => m.id === movieId ? { ...m, in_watchlist: data.added } : m));
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

  // Genre Modal management
  const handleCheckboxChange = (genreId) => {
    setSelectedModalGenres(prev => {
      if (prev.includes(genreId)) {
        return prev.filter(id => id !== genreId);
      }
      if (prev.length >= 4) {
        setModalError('You can select a maximum of 4 genres.');
        setTimeout(() => setModalError(''), 3000);
        return prev;
      }
      return [...prev, genreId];
    });
  };

  const handleModalSubmit = () => {
    if (selectedModalGenres.length === 0) {
      setModalError('Please select at least 1 genre or click Skip.');
      setTimeout(() => setModalError(''), 3000);
      return;
    }

    fetch('/api/profile/save-genres/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ genre_ids: selectedModalGenres })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        setShowModal(false);
        window.location.reload();
      } else {
        alert(data.message || 'Error saving genres.');
      }
    })
    .catch(err => console.error(err));
  };

  // Filter movies for current selected genre
  const filteredGenreMovies = all_movies.filter(m => 
    selectedGenre === 'all' ? true : m.genres && m.genres.includes(selectedGenre)
  );

  return (
    <>
      {/* Header Banner */}
      <header className="w-full pt-32 pb-8 px-gutter md:px-container-padding-desktop max-w-[1440px] mx-auto text-left relative z-10">
        <div className="max-w-4xl py-12">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight uppercase leading-none select-none">
            Discover Films<br />You'll <span className="text-red-600">Love</span>
          </h1>
          <p className="text-white/60 text-lg mt-4 font-medium max-w-xl">
            Search a movie above — we'll find your next obsession.
          </p>
        </div>

        {/* BROWSE BY GENRE Category Pills */}
        <div className="mt-8">
          <h3 className="text-xs font-bold tracking-widest text-white/40 uppercase mb-4">Browse by Genre</h3>
          <div className="flex gap-2.5 overflow-x-auto hide-scrollbar py-2">
            <button
              onClick={() => setSelectedGenre('all')}
              className={`px-5 py-2.5 rounded-full text-sm font-bold transition-all whitespace-nowrap border ${
                selectedGenre === 'all'
                  ? 'bg-red-600 text-white shadow-lg shadow-red-600/20 border-red-600'
                  : 'bg-white/5 text-white/80 hover:bg-white/10 hover:text-white border-white/5'
              }`}
            >
              All
            </button>
            {all_genres.map(g => (
              <button
                key={g.slug}
                onClick={() => setSelectedGenre(g.slug)}
                className={`px-5 py-2.5 rounded-full text-sm font-bold transition-all whitespace-nowrap border ${
                  selectedGenre === g.slug
                    ? 'bg-red-600 text-white shadow-lg shadow-red-600/20 border-red-600'
                    : 'bg-white/5 text-white/80 hover:bg-white/10 hover:text-white border-white/5'
                }`}
              >
                {g.name}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Content Sections */}
      <main className="relative z-10 space-y-section-gap pb-24 text-left">
        {selectedGenre === 'all' ? (
          <div className="space-y-section-gap">
            {/* Continue Watching */}
            {user && continue_watching.length > 0 && (
              <section className="pl-gutter md:pl-container-padding-desktop">
                <h2 className="font-headline-md text-headline-md mb-6 flex items-center gap-2 text-white">
                  Continue Watching
                  <span className="material-symbols-outlined text-primary-container">arrow_forward_ios</span>
                </h2>
                <div className="flex gap-gutter overflow-x-auto hide-scrollbar pb-8">
                  {continue_watching.map(item => {
                    const currentMovieState = moviesState.find(m => m.id === item.movie.id) || item.movie;
                    return (
                      <div key={item.movie.id} className="flex-none w-[320px] aspect-video relative group cursor-pointer transition-all">
                        <div onClick={() => window.location.href = `/movies/${item.movie.id}/watch/`}>
                          <div className="w-full h-full rounded-xl overflow-hidden glass-panel relative aspect-video">
                            <img
                              alt={item.movie.title}
                              className="w-full h-full object-cover group-hover:opacity-50 transition-opacity"
                              src={item.movie.banner_url || item.movie.poster_url}
                              onError={(e) => {
                                e.target.onerror = null;
                                e.target.src = 'https://placehold.co/320x180?text=No+Preview';
                              }}
                            />
                            <div className="absolute bottom-0 left-0 w-full h-1 bg-white/20">
                              <div className="h-full bg-primary-container" style={{ width: `${item.progress}%` }}></div>
                            </div>
                            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                              <span className="material-symbols-outlined text-5xl text-white">play_circle</span>
                            </div>
                          </div>
                          <div className="mt-3">
                            <p className="font-bold text-white truncate">{item.movie.title}</p>
                            <p className="text-sm text-on-surface-variant">{item.progress}% watched</p>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </section>
            )}

            {/* Trending Now */}
            <section className="pl-gutter md:pl-container-padding-desktop">
              <div className="flex justify-between items-center pr-gutter md:pr-container-padding-desktop mb-6">
                <h2 className="font-headline-md text-headline-md text-white">Trending Now</h2>
                <a className="text-primary-container font-bold hover:underline" href="/movies/">See All</a>
              </div>
              <div className="flex gap-gutter overflow-x-auto hide-scrollbar pb-8">
                {trending_movies.map(movie => {
                  const mState = moviesState.find(m => m.id === movie.id) || movie;
                  return (
                    <div
                      key={movie.id}
                      onClick={() => handleCardClick(movie.id)}
                      className="movie-card flex-none w-[220px] aspect-[2/3] rounded-xl overflow-hidden glass-panel relative cursor-pointer group transition-all duration-300 ring-1 ring-white/10"
                    >
                      <img
                        alt={movie.title}
                        className="w-full h-full object-cover"
                        src={movie.poster_url}
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = `https://placehold.co/220x330?text=${encodeURIComponent(movie.title)}`;
                        }}
                      />
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-4">
                        <div className="flex gap-2 mb-4">
                          <button
                            onClick={(e) => handlePlayClick(e, movie.id)}
                            className="bg-white text-black p-2 rounded-full hover:scale-110 transition-transform flex items-center justify-center cursor-pointer"
                          >
                            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
                          </button>
                          <button
                            onClick={(e) => toggleWatchlist(e, movie.id)}
                            className={`p-2 rounded-full hover:scale-110 transition-transform flex items-center justify-center text-white cursor-pointer ${
                              mState.in_watchlist ? 'bg-primary-container' : 'bg-white/20 backdrop-blur-md'
                            }`}
                          >
                            <span className="material-symbols-outlined text-sm">
                              {mState.in_watchlist ? 'check' : 'add'}
                            </span>
                          </button>
                        </div>
                        <p className="font-bold text-lg leading-tight text-white truncate">{movie.title}</p>
                        <div className="flex gap-2 mt-1">
                          <span className="text-xs border border-white/40 px-1 rounded text-white">{movie.release_year}</span>
                          <span className="text-xs text-white/60">{movie.duration}</span>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </section>

            {/* Popular Bento Grid */}
            <section className="px-gutter md:px-container-padding-desktop">
              <h2 className="font-headline-md text-headline-md mb-8 text-white">Popular on CineVerse</h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 h-auto md:h-[500px]">
                {popular_movies[0] ? (
                  <div
                    onClick={() => handleCardClick(popular_movies[0].id)}
                    className="md:col-span-2 rounded-2xl overflow-hidden relative group cursor-pointer glass-panel aspect-video md:aspect-auto"
                  >
                    <img
                      alt={popular_movies[0].title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                      src={popular_movies[0].banner_url || popular_movies[0].poster_url}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-8 flex flex-col justify-end">
                      <span className="bg-red-600 w-fit px-2 py-0.5 rounded text-[10px] font-bold mb-2 text-white">POPULAR</span>
                      <h3 className="text-3xl font-bold mb-2 text-white uppercase leading-none">{popular_movies[0].title}</h3>
                      <p className="text-white/70 max-w-md line-clamp-2">{popular_movies[0].description}</p>
                    </div>
                  </div>
                ) : (
                  <div className="md:col-span-2 rounded-2xl overflow-hidden relative glass-panel flex items-center justify-center">
                    <p className="text-on-surface-variant">No featured popular movie.</p>
                  </div>
                )}

                {popular_movies[1] && (
                  <div
                    onClick={() => handleCardClick(popular_movies[1].id)}
                    className="md:col-span-1 rounded-2xl overflow-hidden relative group cursor-pointer glass-panel aspect-[2/3] md:aspect-auto"
                  >
                    <img
                      alt={popular_movies[1].title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                      src={popular_movies[1].poster_url}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
                      <h3 className="text-xl font-bold text-white truncate">{popular_movies[1].title}</h3>
                    </div>
                  </div>
                )}

                {popular_movies[2] && (
                  <div
                    onClick={() => handleCardClick(popular_movies[2].id)}
                    className="md:col-span-1 rounded-2xl overflow-hidden relative group cursor-pointer glass-panel aspect-[2/3] md:aspect-auto"
                  >
                    <img
                      alt={popular_movies[2].title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                      src={popular_movies[2].poster_url}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
                      <h3 className="text-xl font-bold text-white truncate">{popular_movies[2].title}</h3>
                    </div>
                  </div>
                )}
              </div>
            </section>

            {/* Recommended For You */}
            <section className="pl-gutter md:pl-container-padding-desktop">
              <div className="flex justify-between items-center pr-gutter md:pr-container-padding-desktop mb-6">
                <div>
                  <h2 className="font-headline-md text-headline-md text-white">Recommended for You</h2>
                  {user && payload.profile?.favorite_genres?.length > 0 && (
                    <p className="text-xs text-on-surface-variant mt-1">
                      Based on your favorite genres:{' '}
                      <span className="text-primary-container font-semibold">
                        {payload.profile.favorite_genres.join(', ')}
                      </span>
                    </p>
                  )}
                </div>
                <a className="text-primary-container font-bold hover:underline" href="/movies/">See All</a>
              </div>
              <div className="flex gap-gutter overflow-x-auto hide-scrollbar pb-8">
                {recommended_movies.map(movie => (
                  <div
                    key={movie.id}
                    onClick={() => handleCardClick(movie.id)}
                    className="movie-card flex-none w-[200px] aspect-[2/3] rounded-xl overflow-hidden glass-panel relative cursor-pointer group transition-all duration-300 ring-1 ring-white/10"
                  >
                    <img
                      alt={movie.title}
                      className="w-full h-full object-cover"
                      src={movie.poster_url}
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-4">
                      <p className="font-bold text-base leading-tight text-white mb-2 truncate">{movie.title}</p>
                      <p className="text-xs text-on-surface-variant mb-4">{movie.release_year} • {movie.duration}</p>
                      <div className="flex gap-2">
                        <button
                          onClick={(e) => handlePlayClick(e, movie.id)}
                          className="bg-primary-container text-on-primary-container px-3 py-1.5 rounded-lg font-bold hover:brightness-110 text-xs flex items-center gap-1 cursor-pointer"
                        >
                          <span className="material-symbols-outlined text-xs">play_arrow</span> Play
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCardClick(movie.id);
                          }}
                          className="bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-lg font-bold text-xs flex items-center cursor-pointer"
                        >
                          Info
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Top Rated Masterpieces */}
            <section className="pl-gutter md:pl-container-padding-desktop">
              <div className="flex justify-between items-center pr-gutter md:pr-container-padding-desktop mb-6">
                <h2 className="font-headline-md text-headline-md text-white">Top Rated Masterpieces</h2>
                <a className="text-primary-container font-bold hover:underline" href="/movies/?rating=8">See All</a>
              </div>
              <div className="flex gap-gutter overflow-x-auto hide-scrollbar pb-8">
                {top_rated_movies.map(movie => (
                  <div
                    key={movie.id}
                    onClick={() => handleCardClick(movie.id)}
                    className="movie-card flex-none w-[200px] aspect-[2/3] rounded-xl overflow-hidden glass-panel relative cursor-pointer group transition-all duration-300 ring-1 ring-white/10"
                  >
                    <img
                      alt={movie.title}
                      className="w-full h-full object-cover"
                      src={movie.poster_url}
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-4">
                      <p className="font-bold text-base leading-tight text-white mb-2 truncate">{movie.title}</p>
                      <p className="text-xs text-on-surface-variant mb-4">{movie.release_year} • {movie.duration}</p>
                      <div className="flex gap-2">
                        <button
                          onClick={(e) => handlePlayClick(e, movie.id)}
                          className="bg-primary-container text-on-primary-container px-3 py-1.5 rounded-lg font-bold hover:brightness-110 text-xs flex items-center gap-1 cursor-pointer"
                        >
                          <span className="material-symbols-outlined text-xs">play_arrow</span> Play
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCardClick(movie.id);
                          }}
                          className="bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-lg font-bold text-xs flex items-center cursor-pointer"
                        >
                          Info
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Latest Releases */}
            <section className="pl-gutter md:pl-container-padding-desktop">
              <div className="flex justify-between items-center pr-gutter md:pr-container-padding-desktop mb-6">
                <h2 className="font-headline-md text-headline-md text-white">Latest Releases</h2>
                <a className="text-primary-container font-bold hover:underline" href="/movies/">See All</a>
              </div>
              <div className="flex gap-gutter overflow-x-auto hide-scrollbar pb-8">
                {latest_movies.map(movie => (
                  <div
                    key={movie.id}
                    onClick={() => handleCardClick(movie.id)}
                    className="movie-card flex-none w-[200px] aspect-[2/3] rounded-xl overflow-hidden glass-panel relative cursor-pointer group transition-all duration-300 ring-1 ring-white/10"
                  >
                    <img
                      alt={movie.title}
                      className="w-full h-full object-cover"
                      src={movie.poster_url}
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-4">
                      <p className="font-bold text-base leading-tight text-white mb-2 truncate">{movie.title}</p>
                      <p className="text-xs text-on-surface-variant mb-4">{movie.release_year} • {movie.duration}</p>
                      <div className="flex gap-2">
                        <button
                          onClick={(e) => handlePlayClick(e, movie.id)}
                          className="bg-primary-container text-on-primary-container px-3 py-1.5 rounded-lg font-bold hover:brightness-110 text-xs flex items-center gap-1 cursor-pointer"
                        >
                          <span className="material-symbols-outlined text-xs">play_arrow</span> Play
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCardClick(movie.id);
                          }}
                          className="bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-lg font-bold text-xs flex items-center cursor-pointer"
                        >
                          Info
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        ) : (
          /* Genre Filtered Grid */
          <section className="px-gutter md:px-container-padding-desktop max-w-[1440px] mx-auto pb-24 text-left">
            <h2 className="text-3xl font-extrabold text-white mb-8 uppercase tracking-wider">
              {all_genres.find(g => g.slug === selectedGenre)?.name || selectedGenre}
            </h2>
            {filteredGenreMovies.length === 0 ? (
              <div className="p-12 glass-panel text-center rounded-xl">
                <p className="text-on-surface-variant text-sm">No titles match this genre filter.</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 animate-fade-in">
                {filteredGenreMovies.map(movie => {
                  const mState = moviesState.find(m => m.id === movie.id) || movie;
                  return (
                    <div
                      key={movie.id}
                      onClick={() => handleCardClick(movie.id)}
                      className="movie-card relative aspect-[2/3] rounded-xl overflow-hidden glass-panel cursor-pointer group ring-1 ring-white/10"
                    >
                      <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-md px-2 py-0.5 rounded text-[10px] font-bold text-white uppercase tracking-wider z-20">
                        {all_genres.find(g => g.slug === movie.genres[0])?.name || 'Movie'}
                      </div>
                      <img
                        alt={movie.title}
                        className="w-full h-full object-cover"
                        src={movie.poster_url}
                      />
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-4">
                        <div className="flex gap-2 mb-4">
                          <button
                            onClick={(e) => handlePlayClick(e, movie.id)}
                            className="bg-white text-black p-2 rounded-full hover:scale-110 transition-transform flex items-center justify-center cursor-pointer"
                          >
                            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
                          </button>
                          <button
                            onClick={(e) => toggleWatchlist(e, movie.id)}
                            className={`p-2 rounded-full hover:scale-110 transition-transform flex items-center justify-center text-white cursor-pointer ${
                              mState.in_watchlist ? 'bg-primary-container' : 'bg-white/20 backdrop-blur-md'
                            }`}
                          >
                            <span className="material-symbols-outlined text-sm">
                              {mState.in_watchlist ? 'check' : 'add'}
                            </span>
                          </button>
                        </div>
                        <p className="font-bold text-base leading-tight text-white truncate">{movie.title}</p>
                        <div className="flex gap-2 mt-1">
                          <span className="text-xs border border-white/40 px-1 rounded text-white">{movie.release_year}</span>
                          <span className="text-xs text-white/60">{movie.duration}</span>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </section>
        )}
      </main>

      {/* Genre Selection Modal Popup */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
          <div className="relative w-full max-w-lg p-8 rounded-3xl glass-panel shadow-2xl border border-white/10 flex flex-col justify-between max-h-[90vh] overflow-y-auto">
            <div>
              <div className="text-center mb-8">
                <span className="material-symbols-outlined text-primary-container text-5xl mb-2 animate-pulse" style={{ fontVariationSettings: "'FILL' 1" }}>
                  favorite
                </span>
                <h2 className="text-3xl font-bold text-white tracking-tight">Select Favorite Genres</h2>
                <p className="text-on-surface-variant text-sm mt-2">
                  Pick up to <span className="text-primary-container font-bold">4 genres</span> to personalize your recommendation feed.
                </p>
              </div>

              {modalError && (
                <div className="mb-6 p-4 bg-error-container/20 border border-[#93000a] rounded-xl flex items-center gap-3 text-error text-sm font-semibold">
                  <span className="material-symbols-outlined text-base">error</span>
                  <span>{modalError}</span>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                {all_genres.map(genre => {
                  const isChecked = selectedModalGenres.includes(genre.id);
                  return (
                    <label
                      key={genre.id}
                      className={`relative flex flex-col items-center justify-center p-4 border rounded-2xl cursor-pointer select-none hover:bg-white/10 hover:border-white/20 transition-all text-center group ${
                        isChecked ? 'bg-primary-container/10 border-primary-container/40' : 'bg-white/5 border-white/10'
                      }`}
                    >
                      <input
                        type="checkbox"
                        value={genre.id}
                        checked={isChecked}
                        onChange={() => handleCheckboxChange(genre.id)}
                        className="absolute top-3 right-3 rounded bg-transparent border-white/20 text-primary-container focus:ring-0 cursor-pointer w-4 h-4"
                      />
                      <span className={`font-bold transition-colors mt-2 text-sm ${
                        isChecked ? 'text-primary' : 'text-white group-hover:text-primary-container'
                      }`}>
                        {genre.name}
                      </span>
                    </label>
                  )
                })}
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-white/5 flex gap-4">
              <button
                onClick={() => setShowModal(false)}
                className="w-1/3 py-3.5 border border-white/10 text-white rounded-xl font-bold text-sm hover:bg-white/5 transition-all cursor-pointer"
              >
                Skip
              </button>
              <button
                onClick={handleModalSubmit}
                className="w-2/3 py-3.5 bg-primary-container text-on-primary-container rounded-xl font-bold text-sm hover:brightness-110 transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                Save &amp; Continue
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Home;
