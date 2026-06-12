import { useState } from 'react'

function Profile({ payload, user, csrfToken }) {
  const {
    profile = {},
    genres = [],
    watch_history = [],
    success_message = ''
  } = payload;

  const [username, setUsername] = useState(profile.username || '');
  const [email, setEmail] = useState(profile.email || '');
  const [avatarUrl, setAvatarUrl] = useState(profile.avatar_url || '');
  const [selectedGenres, setSelectedGenres] = useState(profile.favorite_genres || []);
  
  const [errorBanner, setErrorBanner] = useState('');
  const [watchlist, setWatchlist] = useState(profile.watchlist || []);

  const handleCheckboxChange = (genreId) => {
    setSelectedGenres(prev => {
      if (prev.includes(genreId)) {
        return prev.filter(id => id !== genreId);
      }
      if (prev.length >= 4) {
        setErrorBanner('You can select a maximum of 4 genres.');
        setTimeout(() => setErrorBanner(''), 3000);
        return prev;
      }
      return [...prev, genreId];
    });
  };

  const handleCardClick = (id) => {
    window.location.href = `/movies/${id}/`;
  };

  const handlePlayClick = (e, id) => {
    e.stopPropagation();
    e.preventDefault();
    window.location.href = `/movies/${id}/watch/`;
  };

  const removeWatchlist = (e, movieId) => {
    e.stopPropagation();
    e.preventDefault();
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
        window.location.reload();
      }
    })
    .catch(err => console.error(err));
  };

  return (
    <main className="pt-32 pb-section-gap px-gutter max-w-[1440px] mx-auto text-left select-none">
      {/* Profile Header */}
      <header className="mb-section-gap flex flex-col md:flex-row items-center md:items-end gap-8">
        <div className="relative group">
          <div className="w-32 h-32 md:w-48 md:h-48 rounded-full border-4 border-primary-container shadow-[0_0_40px_rgba(229,9,20,0.2)] overflow-hidden bg-surface-container flex items-center justify-center">
            {profile.avatar_url ? (
              <img alt="Large Avatar" className="w-full h-full object-cover" src={profile.avatar_url}/>
            ) : (
              <span className="material-symbols-outlined text-5xl text-white">person</span>
            )}
          </div>
        </div>
        <div className="text-center md:text-left">
          <h1 className="font-headline-lg text-headline-lg mb-2 text-white">{username}</h1>
          <p className="text-on-surface-variant font-body-lg flex items-center justify-center md:justify-start gap-2">
            <span className="material-symbols-outlined text-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>verified</span>
            {profile.subscription_plan} Member
          </p>
        </div>
      </header>

      {success_message && (
        <div className="mb-8 p-4 bg-green-600/20 border border-green-600/30 rounded-xl flex items-center gap-3 text-green-400 text-sm font-semibold">
          <span className="material-symbols-outlined text-base">check_circle</span>
          <span>{success_message}</span>
        </div>
      )}

      {/* Settings Grid */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-section-gap">
        {/* User Details Form */}
        <div className="glass-panel rounded-xl p-8 lg:col-span-2">
          <h2 className="font-headline-md text-headline-md mb-6 text-white">Personal Information</h2>
          <form method="POST" action="/profile/" className="space-y-6">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <label className="block font-label-caps text-on-surface-variant mb-2 text-xs uppercase tracking-wider">Username</label>
                <input 
                  type="text" 
                  name="username" 
                  value={username} 
                  onChange={(e) => setUsername(e.target.value)}
                  required 
                  className="bg-[#1A1D29] border-0 border-b-2 border-white/10 px-4 py-3 focus:border-primary-container focus:ring-0 text-white rounded-t-lg w-full focus:outline-none"
                />
              </div>
              <div>
                <label className="block font-label-caps text-on-surface-variant mb-2 text-xs uppercase tracking-wider">Email Address</label>
                <input 
                  type="email" 
                  name="email" 
                  value={email} 
                  onChange={(e) => setEmail(e.target.value)}
                  required 
                  className="bg-[#1A1D29] border-0 border-b-2 border-white/10 px-4 py-3 focus:border-primary-container focus:ring-0 text-white rounded-t-lg w-full focus:outline-none"
                />
              </div>
              <div className="col-span-full">
                <label className="block font-label-caps text-on-surface-variant mb-2 text-xs uppercase tracking-wider">Avatar URL</label>
                <input 
                  type="url" 
                  name="avatar_url" 
                  value={avatarUrl} 
                  onChange={(e) => setAvatarUrl(e.target.value)}
                  className="bg-[#1A1D29] border-0 border-b-2 border-white/10 px-4 py-3 focus:border-primary-container focus:ring-0 text-white rounded-t-lg w-full focus:outline-none" 
                  placeholder="https://example.com/avatar.jpg"
                />
              </div>
            </div>

            {/* Favorite Genres Selector */}
            <div className="mt-8 pt-6 border-t border-white/5">
              <h3 className="block font-label-caps text-on-surface-variant mb-4 text-xs uppercase tracking-wider">Favorite Genres (Select up to 4)</h3>
              
              {errorBanner && (
                <div className="mb-4 p-4 bg-error-container/20 border border-[#93000a] rounded-xl flex items-center gap-3 text-error text-sm font-semibold">
                  <span className="material-symbols-outlined text-base">error</span>
                  <span>{errorBanner}</span>
                </div>
              )}

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {genres.map(genre => {
                  const isChecked = selectedGenres.includes(genre.id);
                  return (
                    <label 
                      key={genre.id}
                      className={`relative flex flex-col items-center justify-center p-4 border rounded-2xl cursor-pointer select-none hover:bg-white/10 hover:border-white/20 transition-all text-center group ${
                        isChecked ? 'bg-primary-container/10 border-primary-container/40' : 'bg-white/5 border-white/10'
                      }`}
                    >
                      <input 
                        type="checkbox" 
                        name="favorite_genres" 
                        value={genre.id} 
                        checked={isChecked}
                        onChange={() => handleCheckboxChange(genre.id)}
                        className="absolute top-3 right-3 rounded bg-transparent border-white/20 text-primary-container focus:ring-0 cursor-pointer w-4 h-4"
                      />
                      <span className="font-bold text-white group-hover:text-primary-container transition-colors mt-2 text-sm">
                        {genre.name}
                      </span>
                    </label>
                  )
                })}
              </div>
            </div>

            <button type="submit" className="w-full mt-8 py-4 bg-primary-container text-white font-bold rounded-lg hover:brightness-110 transition-all shadow-lg shadow-primary-container/20 cursor-pointer">
              Save Profile Changes
            </button>
          </form>
        </div>

        {/* Subscription Sidebar */}
        <div className="glass-panel rounded-xl p-8 relative overflow-hidden flex flex-col justify-between h-full">
          <div className="absolute top-0 right-0 w-32 h-32 bg-primary-container/10 blur-[60px] rounded-full -mr-16 -mt-16"></div>
          <div>
            <h2 className="font-headline-md text-headline-md mb-6 text-white">Subscription</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-white/60">Current Plan</span>
                <span className="bg-primary-container/20 text-primary-container px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                  {profile.subscription_plan} Tier
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-white/60">Monthly Fee</span>
                <span className="font-bold text-white">
                  {profile.subscription_plan === 'Basic' ? '$8.99' : (profile.subscription_plan === 'Standard' ? '$13.99' : '$19.99')}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-white/60">Billing Cycle</span>
                <span className="font-bold text-white">Monthly</span>
              </div>
            </div>
          </div>
          <a href="/subscription/" className="w-full mt-8 py-3 bg-primary-container text-on-primary-container text-center font-bold rounded-lg hover:brightness-110 transition-all shadow-lg block">
            Upgrade / Change Plan
          </a>
        </div>
      </section>

      {/* Watch History */}
      <section className="mb-section-gap">
        <div className="flex justify-between items-end mb-6">
          <div>
            <h2 className="font-headline-md text-headline-md mb-1 text-white">Watch History</h2>
            <p className="text-on-surface-variant text-sm">Your recently watched streaming activity</p>
          </div>
        </div>
        <div className="flex gap-6 overflow-x-auto pb-4 scroll-smooth hide-scrollbar">
          {watch_history.map((item, idx) => (
            <div 
              key={idx}
              onClick={() => handlePlayClick(null, item.movie.id)}
              className="clickable-card flex-shrink-0 w-[280px] group cursor-pointer"
            >
              <div className="relative aspect-video rounded-xl overflow-hidden mb-3">
                <img 
                  alt={item.movie.title} 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" 
                  src={item.movie.banner_url || item.movie.poster_url} 
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://placehold.co/320x180?text=No+Preview';
                  }}
                />
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="material-symbols-outlined text-5xl text-white">play_circle</span>
                </div>
                <div className="absolute bottom-0 left-0 w-full h-1 bg-white/20">
                  <div className="h-full bg-primary-container" style={{ width: `${item.progress}%` }}></div>
                </div>
              </div>
              <h3 className="font-bold text-white truncate text-left">{item.movie.title}</h3>
              <p className="text-xs text-on-surface-variant text-left">{item.progress}% watched</p>
            </div>
          ))}
          {watch_history.length === 0 && (
            <div className="w-full p-8 glass-panel text-center rounded-xl">
              <p className="text-on-surface-variant text-sm">No streaming activity logged.</p>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

export default Profile;
