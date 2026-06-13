import { useState, useMemo } from 'react'

function AdminDashboard({ payload, csrfToken }) {
  const {
    total_users = 0,
    total_movies = 0,
    monthly_revenue = 0,
    users = [],
    movies = [],
    genres = [],
    selected_content_type = 'movie',
    selected_genre_id = null,
    growth_data = [],
    parent_candidates = []
  } = payload;

  const [activeTab, setActiveTab] = useState(() => {
    return localStorage.getItem('admin-active-tab') || 'overview';
  });

  const [catalogSearch, setCatalogSearch] = useState('');
  const [toast, setToast] = useState(null);

  // Modals state
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingMovie, setEditingMovie] = useState(null);

  // Drag and drop state
  const [draggedMovieId, setDraggedMovieId] = useState(null);
  const [movieListState, setMovieListState] = useState(movies);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4000);
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    localStorage.setItem('admin-active-tab', tab);
  };

  const changeContentType = (contentType) => {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('content_type', contentType);
    localStorage.setItem('admin-active-tab', 'library');
    window.location.href = `?${urlParams.toString()}`;
  };

  const filterByGenre = (genreId) => {
    const urlParams = new URLSearchParams(window.location.search);
    if (genreId) {
      urlParams.set('genre', genreId);
    } else {
      urlParams.delete('genre');
    }
    localStorage.setItem('admin-active-tab', 'library');
    window.location.href = `?${urlParams.toString()}`;
  };

  // Reordering APIs
  const reorderMovie = (movieId, direction) => {
    fetch("/admin-dashboard/catalog/reorder/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 
        movie_id: movieId, 
        direction: direction,
        content_type: selected_content_type,
        genre_id: selected_genre_id
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        showToast('Display order updated.', 'success');
        setTimeout(() => window.location.reload(), 800);
      } else {
        showToast(data.message || 'Error reordering title.', 'error');
      }
    })
    .catch(err => {
      console.error(err);
      showToast('An error occurred.', 'error');
    });
  };

  // Drag & drop handlers
  const handleDragStart = (e, movieId) => {
    setDraggedMovieId(movieId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, index) => {
    e.preventDefault();
    if (draggedMovieId === null) return;
    
    const dragIdx = movieListState.findIndex(m => m.id === draggedMovieId);
    if (dragIdx === index || dragIdx === -1) return;

    const newList = [...movieListState];
    const movedItem = newList[dragIdx];
    newList.splice(dragIdx, 1);
    newList.splice(index, 0, movedItem);
    
    setMovieListState(newList);
  };

  const handleDrop = () => {
    if (draggedMovieId === null) return;
    const movieIds = movieListState.map(m => m.id);

    fetch("/admin-dashboard/catalog/reorder/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 
        movie_ids: movieIds,
        content_type: selected_content_type,
        genre_id: selected_genre_id
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        showToast('Display order updated.', 'success');
      } else {
        showToast(data.message || 'Error updating order.', 'error');
      }
    })
    .catch(err => {
      console.error(err);
      showToast('An error occurred.', 'error');
    })
    .finally(() => {
      setDraggedMovieId(null);
    });
  };

  // Delete Title
  const deleteMovie = (movieId, title) => {
    if (window.confirm(`Are you sure you want to delete "${title}" from the catalog? This action cannot be undone.`)) {
      fetch(`/admin-dashboard/catalog/delete/${movieId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          showToast(`"${title}" deleted successfully.`, 'success');
          setTimeout(() => window.location.reload(), 800);
        } else {
          showToast(data.message || 'Error deleting title.', 'error');
        }
      })
      .catch(err => {
        console.error(err);
        showToast('An error occurred.', 'error');
      });
    }
  };

  // Form submit handlers (AJAX + refresh)
  const handleFormSubmit = (e, successMessage) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const action = form.action;

    fetch(action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => {
      if (res.ok) {
        showToast(successMessage, 'success');
        setIsAddModalOpen(false);
        setIsEditModalOpen(false);
        setTimeout(() => window.location.reload(), 800);
      } else {
        showToast('Error saving title. Check inputs.', 'error');
      }
    })
    .catch(err => {
      console.error(err);
      showToast('An error occurred.', 'error');
    });
  };

  // Open Edit Modal
  const openEditModal = (movie) => {
    // Map movie's genre slugs to genre IDs
    const movieGenreIds = movie.genres.map(slug => {
      const found = genres.find(g => g.slug === slug);
      return found ? found.id : null;
    }).filter(Boolean);

    setEditingMovie({
      ...movie,
      genreIds: movieGenreIds
    });
    setIsEditModalOpen(true);
  };

  // Filter client-side by search query
  const filteredMovies = useMemo(() => {
    if (!catalogSearch.trim()) return movieListState;
    const query = catalogSearch.toLowerCase().trim();
    return movieListState.filter(m => m.title.toLowerCase().includes(query));
  }, [movieListState, catalogSearch]);

  return (
    <main className="pt-24 pb-section-gap px-gutter max-w-[1440px] mx-auto text-left select-none">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h2 className="font-headline-lg text-headline-lg text-white font-bold">System Admin</h2>
          <p className="text-on-surface-variant font-body-md text-sm mt-1">
            Administrator panel. Monitoring site activity, movies catalog, and subscriptions.
          </p>
        </div>
      </header>

      {/* Tabs Navigation */}
      <div className="flex gap-4 border-b border-white/10 mb-8">
        <button
          onClick={() => handleTabChange('overview')}
          className={`px-6 py-3 border-b-2 font-bold text-sm transition-all focus:outline-none ${
            activeTab === 'overview' ? 'border-primary-container text-primary-container' : 'border-transparent text-on-surface-variant hover:text-white'
          }`}
        >
          System Overview
        </button>
        <button
          onClick={() => handleTabChange('library')}
          className={`px-6 py-3 border-b-2 font-bold text-sm transition-all focus:outline-none flex items-center gap-2 ${
            activeTab === 'library' ? 'border-primary-container text-primary-container' : 'border-transparent text-on-surface-variant hover:text-white'
          }`}
        >
          <span className="material-symbols-outlined text-sm">movie_filter</span> Manage Catalog
        </button>
      </div>

      {/* PANEL 1: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="space-y-10">
          {/* Stats Grid */}
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="glass-panel p-6 rounded-2xl group hover:border-primary-container/30 transition-all duration-500">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 bg-primary-container/10 rounded-xl">
                  <span className="material-symbols-outlined text-primary-container">group</span>
                </div>
                <span className="text-green-400 font-label-caps text-xs flex items-center gap-1">
                  <span className="material-symbols-outlined text-sm">trending_up</span> +12%
                </span>
              </div>
              <h3 className="text-on-surface-variant font-label-caps mb-1 text-xs uppercase tracking-wider font-bold">Total Accounts</h3>
              <p className="text-3xl font-headline-md font-bold text-white">{total_users}</p>
            </div>

            <div className="glass-panel p-6 rounded-2xl group hover:border-primary-container/30 transition-all duration-500">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 bg-primary-container/10 rounded-xl">
                  <span className="material-symbols-outlined text-primary-container">movie_filter</span>
                </div>
                <span className="text-on-surface-variant/50 font-label-caps text-xs">Stable</span>
              </div>
              <h3 className="text-on-surface-variant font-label-caps mb-1 text-xs uppercase tracking-wider font-bold">Catalog Library</h3>
              <p className="text-3xl font-headline-md font-bold text-white">{total_movies}</p>
            </div>

            <div className="glass-panel p-6 rounded-2xl group hover:border-primary-container/30 transition-all duration-500">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 bg-primary-container/10 rounded-xl">
                  <span className="material-symbols-outlined text-primary-container">card_membership</span>
                </div>
                <span className="text-green-400 font-label-caps text-xs flex items-center gap-1">
                  <span className="material-symbols-outlined text-sm">trending_up</span> +8.4%
                </span>
              </div>
              <h3 className="text-on-surface-variant font-label-caps mb-1 text-xs uppercase tracking-wider font-bold">Paid Tiers</h3>
              <p className="text-3xl font-headline-md font-bold text-white">{total_users}</p>
            </div>

            <div className="glass-panel p-6 rounded-2xl group hover:border-primary-container/30 transition-all duration-500">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 bg-primary-container/10 rounded-xl">
                  <span className="material-symbols-outlined text-primary-container">payments</span>
                </div>
                <span className="text-green-400 font-label-caps text-xs flex items-center gap-1">
                  <span className="material-symbols-outlined text-sm">trending_up</span> +15%
                </span>
              </div>
              <h3 className="text-on-surface-variant font-label-caps mb-1 text-xs uppercase tracking-wider font-bold">Est. Monthly Revenue</h3>
              <p className="text-3xl font-headline-md font-bold text-white">${monthly_revenue}</p>
            </div>
          </section>

          {/* Visualization Section */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 glass-panel p-6 rounded-2xl">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h4 className="font-headline-md text-headline-md text-white font-bold">Subscriber Growth</h4>
                  <p className="text-on-surface-variant text-sm mt-1">Year-to-date performance</p>
                </div>
                <div className="flex gap-2">
                  <button type="button" className="px-3 py-1 bg-white/5 rounded-lg text-xs hover:bg-white/10 text-white">W</button>
                  <button type="button" className="px-3 py-1 bg-primary-container text-white rounded-lg text-xs">M</button>
                  <button type="button" className="px-3 py-1 bg-white/5 rounded-lg text-xs hover:bg-white/10 text-white">Y</button>
                </div>
              </div>
              <div className="h-64 relative flex items-end gap-2 overflow-hidden">
                {growth_data.map((d, index) => {
                  const maxVal = Math.max(...growth_data.map(item => item.count), 1);
                  const pct = (d.count / maxVal) * 100;
                  return (
                    <div 
                      key={index} 
                      style={{ height: `${pct}%` }} 
                      className="flex-1 bg-primary-container/30 rounded-t-lg hover:bg-primary-container/50 transition-all duration-300 relative group cursor-pointer"
                    >
                      <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-[#1E2020] p-2 rounded text-[10px] opacity-0 group-hover:opacity-100 transition-opacity text-white z-20 whitespace-nowrap">
                        {d.count}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="flex justify-between mt-4 text-on-surface-variant font-label-caps opacity-50 text-xs text-white">
                {growth_data.map((d, index) => (
                  <span key={index} className="flex-1 text-center">{d.month}</span>
                ))}
              </div>
            </div>

            <div className="glass-panel p-6 rounded-2xl flex flex-col items-center justify-center text-center">
              <h4 className="font-headline-md text-headline-md mb-2 text-white font-bold">User Retention</h4>
              <div className="relative w-40 h-40 mb-6">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="80" cy="80" fill="transparent" r="70" stroke="rgba(255,255,255,0.05)" strokeWidth="12"></circle>
                  <circle cx="80" cy="80" fill="transparent" r="70" stroke="#E50914" strokeDasharray="440" stroke-dashoffset="88" strokeLinecap="round" strokeWidth="12"></circle>
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">82%</span>
                </div>
              </div>
              <div className="space-y-3 w-full">
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center gap-2 text-white"><span className="w-2 h-2 rounded-full bg-primary-container"></span> Returning</span>
                  <span className="font-bold text-white">82%</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center gap-2 text-white"><span className="w-2 h-2 rounded-full bg-white/20"></span> New</span>
                  <span className="font-bold text-white">18%</span>
                </div>
              </div>
            </div>
          </section>

          {/* Tables Row */}
          <section className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            {/* New registrations */}
            <div className="glass-panel rounded-2xl overflow-hidden">
              <div className="p-6 border-b border-white/5 flex justify-between items-center">
                <h4 className="font-headline-md text-headline-md text-white font-bold">New Registrations</h4>
              </div>
              <div className="overflow-x-auto">
                <table class="w-full text-left">
                  <thead>
                    <tr className="text-on-surface-variant/50 font-label-caps text-xs border-b border-white/5 text-white/50">
                      <th className="px-6 py-4 uppercase">User</th>
                      <th className="px-6 py-4 uppercase">Plan</th>
                      <th className="px-6 py-4 uppercase">Status</th>
                      <th className="px-6 py-4 text-right uppercase">Joined Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {users.map(u => (
                      <tr key={u.id} className="hover:bg-white/5 transition-colors group">
                        <td className="px-6 py-4 flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center text-xs font-bold text-white uppercase">
                            {u.username.slice(0, 2)}
                          </div>
                          <span className="font-medium text-white">{u.username}</span>
                        </td>
                        <td className="px-6 py-4 text-on-surface-variant text-white/70">{u.subscription_plan}</td>
                        <td className="px-6 py-4">
                          <span className="px-2 py-0.5 rounded-full bg-green-500/20 text-green-400 text-[10px]">ACTIVE</span>
                        </td>
                        <td className="px-6 py-4 text-right text-on-surface-variant text-white/70 text-sm">
                          {u.date_joined}
                        </td>
                      </tr>
                    ))}
                    {users.length === 0 && (
                      <tr>
                        <td colSpan="4" className="p-6 text-center text-on-surface-variant text-sm">No registered accounts.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Library Updates */}
            <div className="glass-panel rounded-2xl overflow-hidden">
              <div className="p-6 border-b border-white/5 flex justify-between items-center">
                <h4 className="font-headline-md text-headline-md text-white font-bold">Library Updates</h4>
                <button
                  onClick={() => handleTabChange('library')}
                  className="text-primary-container font-label-caps text-xs font-bold hover:underline transition-all"
                >
                  MANAGE CATALOG
                </button>
              </div>
              <div className="p-6 space-y-4">
                {movies.slice(0, 4).map(movie => (
                  <div key={movie.id} className="flex items-center gap-4 group">
                    <div className="w-12 h-16 rounded overflow-hidden flex-shrink-0 bg-surface-container">
                      <img
                        alt={movie.title}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                        src={movie.poster_url}
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = `https://placehold.co/300x450?text=${encodeURIComponent(movie.title)}`;
                        }}
                      />
                    </div>
                    <div className="flex-1 text-left">
                      <p className="font-bold text-on-background text-white">{movie.title}</p>
                      <p className="text-xs text-on-surface-variant mt-0.5">
                        {movie.genres && movie.genres.length > 0 ? movie.genres[0] : 'No Genre'} • {movie.release_year} • {movie.language}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-[10px] text-on-surface-variant font-label-caps uppercase text-white/50">Rating</p>
                      <p className="text-xs text-white font-bold mt-0.5">{movie.rating}</p>
                    </div>
                  </div>
                ))}
                {movies.length === 0 && (
                  <p className="text-on-surface-variant text-sm text-center">No movies in the catalog library.</p>
                )}
              </div>
            </div>
          </section>
        </div>
      )}

      {/* PANEL 2: MANAGE CATALOG */}
      {activeTab === 'library' && (
        <div className="space-y-6">
          <div className="glass-panel rounded-2xl overflow-hidden">
            {/* Search & Actions */}
            <div className="p-6 border-b border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <h4 className="font-headline-md text-headline-md text-white font-bold flex items-center gap-2">
                <span className="material-symbols-outlined text-primary-container">movie_filter</span> Library Catalog
              </h4>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">search</span>
                  <input
                    type="text"
                    value={catalogSearch}
                    onChange={(e) => setCatalogSearch(e.target.value)}
                    placeholder="Search catalog..."
                    className="bg-white/5 border border-white/10 rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-primary-container transition-colors w-48 sm:w-64"
                  />
                </div>
                <button
                  onClick={() => setIsAddModalOpen(true)}
                  className="px-4 py-2 bg-primary-container text-white rounded-lg font-bold text-sm hover:brightness-110 transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <span className="material-symbols-outlined text-sm">add</span> Add Title
                </button>
              </div>
            </div>

            {/* Segment Controls & Genre dropdown */}
            <div className="p-6 bg-white/[0.02] border-b border-white/5 flex flex-col md:flex-row gap-4 items-center justify-between">
              <div className="flex gap-2 bg-white/5 p-1 rounded-xl border border-white/5 w-full md:w-auto">
                <button
                  onClick={() => changeContentType('movie')}
                  className={`flex-1 md:flex-initial text-center px-6 py-2 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
                    selected_content_type === 'movie' ? 'bg-primary-container text-white' : 'text-on-surface-variant hover:text-white'
                  }`}
                >
                  Movies
                </button>
                <button
                  onClick={() => changeContentType('series')}
                  className={`flex-1 md:flex-initial text-center px-6 py-2 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
                    selected_content_type === 'series' ? 'bg-primary-container text-white' : 'text-on-surface-variant hover:text-white'
                  }`}
                >
                  Series
                </button>
              </div>

              <div className="flex items-center gap-3 w-full md:w-auto justify-end">
                <label className="text-xs font-bold text-on-surface-variant uppercase whitespace-nowrap text-white/50">Filter Genre:</label>
                <select
                  value={selected_genre_id || ''}
                  onChange={(e) => filterByGenre(e.target.value)}
                  className="bg-[#1A1C1E] border border-white/10 rounded-lg px-4 py-2 text-white text-sm focus:outline-none focus:border-primary-container transition-colors w-full md:w-48 cursor-pointer"
                >
                  <option value="">All Genres</option>
                  {genres.map(g => (
                    <option key={g.id} value={g.id}>{g.name}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Movies/Series Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-on-surface-variant/50 font-label-caps text-xs border-b border-white/5 text-white/50">
                    <th className="px-6 py-4 uppercase">Title</th>
                    <th className="px-6 py-4 uppercase">Genres</th>
                    <th className="px-6 py-4 text-center uppercase">Reorder</th>
                    <th className="px-6 py-4 text-center uppercase">Collections</th>
                    <th className="px-6 py-4 text-right uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody
                  className="divide-y divide-white/5"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleDrop}
                >
                  {filteredMovies.map((movie, index) => (
                    <tr
                      key={movie.id}
                      draggable
                      onDragStart={(e) => handleDragStart(e, movie.id)}
                      onDragOver={(e) => handleDragOver(e, index)}
                      className={`hover:bg-white/5 transition-colors border-b border-white/5 ${
                        draggedMovieId === movie.id ? 'opacity-40 bg-primary-container/10 border-dashed border-primary-container/30' : ''
                      }`}
                    >
                      <td className="px-6 py-4 flex items-center gap-3">
                        <span className="material-symbols-outlined text-white/20 hover:text-white/80 select-none mr-1 cursor-grab" title="Drag to reorder">
                          drag_indicator
                        </span>
                        <img
                          src={movie.poster_url}
                          className="w-10 h-14 object-cover rounded bg-white/5 flex-shrink-0"
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = `https://placehold.co/300x450?text=${encodeURIComponent(movie.title)}`;
                          }}
                        />
                        <div className="text-left">
                          <p className="font-bold text-white leading-tight">{movie.title}</p>
                          <p className="text-xs text-on-surface-variant mt-1">
                            {movie.content_type.toUpperCase()} • {movie.release_year} • {movie.duration}
                          </p>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-on-surface-variant text-white/70">
                        {movie.genres && movie.genres.length > 0 ? movie.genres.join(', ') : 'None'}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <button
                            onClick={() => reorderMovie(movie.id, 'up')}
                            className="p-1 hover:bg-white/10 text-white rounded transition-colors flex items-center justify-center cursor-pointer"
                            title="Move Up"
                          >
                            <span className="material-symbols-outlined text-sm">arrow_upward</span>
                          </button>
                          <button
                            onClick={() => reorderMovie(movie.id, 'down')}
                            className="p-1 hover:bg-white/10 text-white rounded transition-colors flex items-center justify-center cursor-pointer"
                            title="Move Down"
                          >
                            <span className="material-symbols-outlined text-sm">arrow_downward</span>
                          </button>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="flex items-center justify-center gap-1.5 flex-wrap">
                          {movie.is_trending && <span className="px-1.5 py-0.5 rounded bg-primary-container/20 text-primary-container text-[9px] font-bold">TRENDING</span>}
                          {movie.is_popular && <span className="px-1.5 py-0.5 rounded bg-green-500/20 text-green-400 text-[9px] font-bold">POPULAR</span>}
                          {movie.is_latest && <span className="px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 text-[9px] font-bold">LATEST</span>}
                          {movie.is_top_rated && <span className="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 text-[9px] font-bold">TOP</span>}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-right flex items-center justify-end gap-2">
                        <button
                          onClick={() => openEditModal(movie)}
                          className="p-2 hover:bg-white/10 text-white rounded-lg transition-colors inline-flex items-center justify-center cursor-pointer"
                          title="Edit Title"
                        >
                          <span className="material-symbols-outlined text-sm">edit</span>
                        </button>
                        <button
                          onClick={() => deleteMovie(movie.id, movie.title)}
                          className="p-2 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors inline-flex items-center justify-center cursor-pointer"
                          title="Delete Movie"
                        >
                          <span className="material-symbols-outlined text-sm">delete</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                  {filteredMovies.length === 0 && (
                    <tr>
                      <td colSpan="5" className="p-6 text-center text-on-surface-variant text-sm">No items in the catalog library.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Add Title Modal */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm transition-all duration-300">
          <div className="glass-panel max-w-2xl w-full mx-4 rounded-2xl overflow-hidden shadow-2xl border border-white/10 flex flex-col max-h-[85vh]">
            <div className="p-6 border-b border-white/5 flex items-center justify-between">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span className="material-symbols-outlined text-primary-container">movie</span> Add New Title
              </h3>
              <button
                onClick={() => setIsAddModalOpen(false)}
                className="p-1 hover:bg-white/10 rounded-full text-white/60 hover:text-white transition-colors"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
            
            <form
              action="/admin-dashboard/catalog/add/"
              method="POST"
              onSubmit={(e) => handleFormSubmit(e, 'Title added successfully!')}
              className="p-6 overflow-y-auto space-y-4 flex-1 text-left"
            >
              <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="md:col-span-2">
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Title</label>
                  <input type="text" name="title" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Content Type</label>
                  <select name="content_type" className="w-full bg-[#1A1C1E] border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors">
                    <option value="movie">Movie</option>
                    <option value="series">Series (TV Show)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Description</label>
                <textarea name="description" required rows="3" className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"></textarea>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Poster URL</label>
                  <input type="url" name="poster_url" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="https://image.tmdb.org/t/p/..." />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Banner (Backdrop) URL</label>
                  <input type="url" name="banner_url" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="https://image.tmdb.org/t/p/..." />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Video URL</label>
                  <input type="url" name="video_url" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="https://example.com/video.mp4" defaultValue="https://www.w3schools.com/html/mov_bbb.mp4" />
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Rating (0-10)</label>
                  <input type="number" step="0.1" name="rating" min="0" max="10" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" defaultValue="8.0" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Release Year</label>
                  <input type="number" name="release_year" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" defaultValue="2024" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Language</label>
                  <input type="text" name="language" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" defaultValue="English" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Duration</label>
                  <input type="text" name="duration" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" defaultValue="2h 15m" placeholder="e.g. 2h 15m or TV Series" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Parent Franchise / Series</label>
                  <select name="parent_id" className="w-full bg-[#1A1C1E] border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors">
                    <option value="none">None (Is a Parent / Standalone)</option>
                    {parent_candidates.map(p => (
                      <option key={p.id} value={p.id}>{p.title}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Part / Season Number</label>
                  <input type="number" name="part_number" className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="e.g. 1 or 2" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Part / Season Name</label>
                  <input type="text" name="part_name" className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="e.g. Season 1 or Homecoming" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Cast (Comma separated)</label>
                  <input type="text" name="cast" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" placeholder="Actor 1, Actor 2" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Crew (Comma separated)</label>
                  <input type="text" name="crew" required className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" defaultValue="Director: John Doe" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-2 uppercase text-white/70">Genres</label>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 bg-white/5 p-4 rounded-xl border border-white/5">
                  {genres.map(g => (
                    <label key={g.id} className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                      <input type="checkbox" name="genres" value={g.id} className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 focus:ring-offset-0 cursor-pointer" />
                      {g.name}
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-2 uppercase text-white/70">Collection Placement Flags</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input type="checkbox" name="is_trending" className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer" />
                    Trending
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input type="checkbox" name="is_popular" className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer" />
                    Popular
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input type="checkbox" name="is_latest" className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer" />
                    Latest
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input type="checkbox" name="is_top_rated" className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer" />
                    Top Rated
                  </label>
                </div>
              </div>

              <div className="pt-4 border-t border-white/5 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="px-6 py-2.5 rounded-lg border border-white/15 text-white hover:bg-white/10 font-bold transition-all text-sm cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-lg bg-primary-container text-white hover:brightness-110 font-bold transition-all text-sm cursor-pointer"
                >
                  Add Title
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Title Modal */}
      {isEditModalOpen && editingMovie && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm transition-all duration-300">
          <div className="glass-panel max-w-2xl w-full mx-4 rounded-2xl overflow-hidden shadow-2xl border border-white/10 flex flex-col max-h-[85vh]">
            <div className="p-6 border-b border-white/5 flex items-center justify-between">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span className="material-symbols-outlined text-primary-container">edit</span> Edit Title Catalog
              </h3>
              <button
                onClick={() => setIsEditModalOpen(false)}
                className="p-1 hover:bg-white/10 rounded-full text-white/60 hover:text-white transition-colors"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form
              action={`/admin-dashboard/catalog/edit/${editingMovie.id}/`}
              method="POST"
              onSubmit={(e) => handleFormSubmit(e, 'Title updated successfully!')}
              className="p-6 overflow-y-auto space-y-4 flex-1 text-left"
            >
              <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="md:col-span-2">
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Title</label>
                  <input
                    type="text"
                    name="title"
                    defaultValue={editingMovie.title}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Content Type</label>
                  <select
                    name="content_type"
                    defaultValue={editingMovie.content_type}
                    className="w-full bg-[#1A1C1E] border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  >
                    <option value="movie">Movie</option>
                    <option value="series">Series (TV Show)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Description</label>
                <textarea
                  name="description"
                  defaultValue={editingMovie.description}
                  required
                  rows="3"
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                ></textarea>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Poster URL</label>
                  <input
                    type="url"
                    name="poster_url"
                    defaultValue={editingMovie.poster_url}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Banner (Backdrop) URL</label>
                  <input
                    type="url"
                    name="banner_url"
                    defaultValue={editingMovie.banner_url}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Video URL</label>
                  <input
                    type="url"
                    name="video_url"
                    defaultValue={editingMovie.video_url}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Rating (0-10)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="rating"
                    defaultValue={editingMovie.rating}
                    min="0"
                    max="10"
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Release Year</label>
                  <input
                    type="number"
                    name="release_year"
                    defaultValue={editingMovie.release_year}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Language</label>
                  <input
                    type="text"
                    name="language"
                    defaultValue={editingMovie.language}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Duration</label>
                  <input
                    type="text"
                    name="duration"
                    defaultValue={editingMovie.duration}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Parent Franchise / Series</label>
                  <select 
                    name="parent_id" 
                    defaultValue={editingMovie.parent_id || 'none'}
                    className="w-full bg-[#1A1C1E] border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  >
                    <option value="none">None (Is a Parent / Standalone)</option>
                    {parent_candidates.filter(p => p.id !== editingMovie.id).map(p => (
                      <option key={p.id} value={p.id}>{p.title}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Part / Season Number</label>
                  <input 
                    type="number" 
                    name="part_number" 
                    defaultValue={editingMovie.part_number || ''}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" 
                    placeholder="e.g. 1 or 2" 
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Part / Season Name</label>
                  <input 
                    type="text" 
                    name="part_name" 
                    defaultValue={editingMovie.part_name || ''}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors" 
                    placeholder="e.g. Season 1 or Homecoming" 
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Cast</label>
                  <input
                    type="text"
                    name="cast"
                    defaultValue={editingMovie.cast}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-on-surface-variant mb-1 uppercase text-white/70">Crew</label>
                  <input
                    type="text"
                    name="crew"
                    defaultValue={editingMovie.crew}
                    required
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-container transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-2 uppercase text-white/70">Genres</label>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 bg-white/5 p-4 rounded-xl border border-white/5">
                  {genres.map(g => (
                    <label key={g.id} className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                      <input
                        type="checkbox"
                        name="genres"
                        value={g.id}
                        defaultChecked={editingMovie.genreIds?.includes(g.id)}
                        className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 focus:ring-offset-0 cursor-pointer"
                      />
                      {g.name}
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-on-surface-variant mb-2 uppercase text-white/70">Collection Placement Flags</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input
                      type="checkbox"
                      name="is_trending"
                      defaultChecked={editingMovie.is_trending}
                      className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer"
                    />
                    Trending
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input
                      type="checkbox"
                      name="is_popular"
                      defaultChecked={editingMovie.is_popular}
                      className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer"
                    />
                    Popular
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input
                      type="checkbox"
                      name="is_latest"
                      defaultChecked={editingMovie.is_latest}
                      className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer"
                    />
                    Latest
                  </label>
                  <label className="flex items-center gap-2 text-white text-sm cursor-pointer select-none">
                    <input
                      type="checkbox"
                      name="is_top_rated"
                      defaultChecked={editingMovie.is_top_rated}
                      className="rounded bg-white/5 border-white/10 text-primary focus:ring-0 cursor-pointer"
                    />
                    Top Rated
                  </label>
                </div>
              </div>

              <div className="pt-4 border-t border-white/5 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsEditModalOpen(false)}
                  className="px-6 py-2.5 rounded-lg border border-white/15 text-white hover:bg-white/10 font-bold transition-all text-sm cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-lg bg-primary-container text-white hover:brightness-110 font-bold transition-all text-sm cursor-pointer"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Toast Notification Container */}
      {toast && (
        <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-3 pointer-events-none">
          <div
            className={`glass-panel px-6 py-4 rounded-xl shadow-2xl border flex items-center gap-3 text-sm font-semibold transition-all duration-300 pointer-events-auto cursor-pointer max-w-sm ${
              toast.type === 'success' ? 'border-green-500/30 bg-green-500/10 text-green-400' : 'border-red-500/30 bg-red-500/10 text-red-400'
            }`}
          >
            <span className="material-symbols-outlined text-base">
              {toast.type === 'success' ? 'check_circle' : 'error'}
            </span>
            <span>{toast.message}</span>
          </div>
        </div>
      )}
    </main>
  );
}

export default AdminDashboard;
