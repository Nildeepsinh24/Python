import { useState, useEffect } from 'react'

function Layout({ children, user, userAvatar, userEmail, isSuperuser, csrfToken, page }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);

  // Monitor scroll for header background transitions
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="font-body-md text-body-md min-h-screen flex flex-col justify-between text-on-background">
      {/* Top Navigation Bar */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ease-in-out border-b border-white/5 shadow-2xl ${
        scrolled ? 'bg-[#08090C]/95 py-2' : 'bg-[#08090C]/90 py-3 md:py-4'
      }`}>
        <div className="max-w-[1440px] mx-auto px-gutter flex flex-col gap-3">
          {/* Row 1: Logo, Desktop Links, Actions, Hamburger */}
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-8">
              <a href="/" className="text-2xl font-black tracking-wider text-red-600 select-none">CINEVERSE</a>
              {/* Desktop Links */}
              <div className="hidden lg:flex items-center gap-6">
                <a className={`text-sm ${page === 'home' ? 'text-red-500 font-bold' : 'text-white/70 font-medium hover:text-white transition-colors duration-300'}`} href="/">Home</a>
                <a className={`text-sm ${page === 'movie_list' && !window.location.search.includes('series') ? 'text-red-500 font-bold' : 'text-white/70 font-medium hover:text-white transition-colors duration-300'}`} href="/movies/?content_type=movie">Movies</a>
                <a className={`text-sm ${page === 'movie_list' && window.location.search.includes('series') ? 'text-red-500 font-bold' : 'text-white/70 font-medium hover:text-white transition-colors duration-300'}`} href="/movies/?content_type=series">Series</a>
                <a className={`text-sm ${page === 'subscription' ? 'text-red-500 font-bold' : 'text-white/70 font-medium hover:text-white transition-colors duration-300'}`} href="/subscription/">Plans</a>
                {user && (
                  <a className={`text-sm ${page === 'dashboard' ? 'text-red-500 font-bold' : 'text-white/70 font-medium hover:text-white transition-colors duration-300'}`} href="/dashboard/">My List</a>
                )}
              </div>
            </div>

            {/* Right side controls */}
            <div className="flex items-center gap-4">
              {/* Desktop Search Pill */}
              <div className="hidden md:block w-72 lg:w-96">
                <form action="/search/" method="GET" className="relative flex items-center bg-[#151821] border border-white/10 rounded-full p-1 w-full shadow-inner">
                  <input
                    name="q"
                    type="text"
                    className="bg-transparent border-none focus:ring-0 text-white placeholder-white/40 text-xs pl-4 pr-16 py-1.5 w-full focus:outline-none"
                    placeholder="Search a movie to get recommendation..."
                  />
                  <button type="submit" className="absolute right-1 bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-3 py-1.5 rounded-full transition-colors">Find</button>
                </form>
              </div>

              {/* User Actions */}
              <div className="flex items-center gap-3">
                {user ? (
                  <div className="relative">
                    <div 
                      onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                      className="w-9 h-9 rounded-full border-2 border-white/10 overflow-hidden cursor-pointer hover:scale-105 transition-transform flex items-center justify-center bg-surface-container"
                    >
                      {userAvatar ? (
                        <img alt="User Profile" className="w-full h-full object-cover" src={userAvatar}/>
                      ) : (
                        <span className="material-symbols-outlined text-white text-base">person</span>
                      )}
                    </div>
                    {/* Dropdown Menu */}
                    {profileDropdownOpen && (
                      <>
                        <div className="fixed inset-0 z-40" onClick={() => setProfileDropdownOpen(false)}></div>
                        <div className="absolute right-0 mt-2 w-48 bg-surface-container border border-white/10 rounded-xl shadow-2xl py-2 z-50">
                          <div className="px-4 py-2 border-b border-white/5">
                            <p className="font-bold truncate text-white text-xs">{user}</p>
                            <p className="text-[10px] text-white/50 truncate">{userEmail}</p>
                          </div>
                          <a href="/dashboard/" className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 text-xs text-white/70 hover:text-white transition-colors">
                            <span className="material-symbols-outlined text-sm">dashboard</span> Dashboard
                          </a>
                          <a href="/profile/" className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 text-xs text-white/70 hover:text-white transition-colors">
                            <span className="material-symbols-outlined text-sm">settings</span> Profile Settings
                          </a>
                          {isSuperuser && (
                            <a href="/admin-dashboard/" className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 text-xs text-white/70 hover:text-white transition-colors">
                              <span class="material-symbols-outlined text-sm">admin_panel_settings</span> Admin Dashboard
                            </a>
                          )}
                          <a href="/logout/" className="flex items-center gap-2 px-4 py-2 hover:bg-white/5 text-xs text-red-500 font-bold transition-colors">
                            <span className="material-symbols-outlined text-sm text-red-500">logout</span> Logout
                          </a>
                        </div>
                      </>
                    )}
                  </div>
                ) : (
                  <>
                    <a href="/login/" className="px-3 py-1.5 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700 transition-colors text-xs">Sign In</a>
                    <a href="/register/" className="px-3 py-1.5 border border-white/20 text-white font-bold rounded-lg hover:bg-white/5 transition-colors text-xs hidden sm:inline-block">Register</a>
                  </>
                )}
              </div>

              {/* Hamburger Button (Mobile Only) */}
              <button 
                onClick={() => setMobileDrawerOpen(true)}
                className="lg:hidden p-2 text-white hover:text-red-500 transition-colors flex items-center justify-center"
              >
                <span className="material-symbols-outlined text-2xl">menu</span>
              </button>
            </div>
          </div>

          {/* Row 2: Mobile Search Pill */}
          <div className="w-full md:hidden">
            <form action="/search/" method="GET" className="relative flex items-center bg-[#151821] border border-white/10 rounded-full p-1 w-full shadow-inner">
              <input
                name="q"
                type="text"
                className="bg-transparent border-none focus:ring-0 text-white placeholder-white/40 text-xs pl-4 pr-16 py-1.5 w-full focus:outline-none"
                placeholder="Search a movie to get recommendation..."
              />
              <button type="submit" className="absolute right-1 bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-4 py-1.5 rounded-full transition-colors">Find</button>
            </form>
          </div>
        </div>
      </nav>

      {/* Mobile Drawer Overlay Menu */}
      {mobileDrawerOpen && (
        <>
          <div 
            onClick={() => setMobileDrawerOpen(false)}
            className="fixed inset-0 bg-black/80 backdrop-blur-md z-[90] transition-opacity duration-300 opacity-100 lg:hidden"
          ></div>
          <div className="fixed inset-y-0 right-0 w-64 bg-[#09090B] border-l border-white/10 shadow-2xl p-6 flex flex-col gap-6 z-[100] transition-transform duration-300 ease-in-out lg:hidden transform translate-x-0">
            <div className="flex items-center justify-between pb-4 border-b border-white/5">
              <span className="text-lg font-bold text-red-600">MENU</span>
              <button 
                onClick={() => setMobileDrawerOpen(false)}
                className="p-1 text-white/70 hover:text-white transition-colors"
              >
                <span className="material-symbols-outlined text-xl">close</span>
              </button>
            </div>
            <div className="flex flex-col gap-2">
              <a className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-all ${page === 'home' ? 'text-red-500 bg-red-500/10 font-bold' : 'text-white/70 font-medium hover:text-white hover:bg-white/5'}`} href="/">
                <span className="material-symbols-outlined text-lg">home</span>
                <span>Home</span>
              </a>
              <a className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-all ${page === 'movie_list' && !window.location.search.includes('series') ? 'text-red-500 bg-red-500/10 font-bold' : 'text-white/70 font-medium hover:text-white hover:bg-white/5'}`} href="/movies/?content_type=movie">
                <span className="material-symbols-outlined text-lg">movie</span>
                <span>Movies</span>
              </a>
              <a className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-all ${page === 'movie_list' && window.location.search.includes('series') ? 'text-red-500 bg-red-500/10 font-bold' : 'text-white/70 font-medium hover:text-white hover:bg-white/5'}`} href="/movies/?content_type=series">
                <span className="material-symbols-outlined text-lg">live_tv</span>
                <span>Series</span>
              </a>
              <a className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-all ${page === 'subscription' ? 'text-red-500 bg-red-500/10 font-bold' : 'text-white/70 font-medium hover:text-white hover:bg-white/5'}`} href="/subscription/">
                <span className="material-symbols-outlined text-lg">card_membership</span>
                <span>Plans</span>
              </a>
              {user && (
                <a className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-all ${page === 'dashboard' ? 'text-red-500 bg-red-500/10 font-bold' : 'text-white/70 font-medium hover:text-white hover:bg-white/5'}`} href="/dashboard/">
                  <span className="material-symbols-outlined text-lg">playlist_add_check</span>
                  <span>My List</span>
                </a>
              )}
            </div>
          </div>
        </>
      )}

      {/* Main Content Area */}
      <div className="flex-grow">
        {children}
      </div>

      {/* Footer */}
      <footer className="w-full py-section-gap bg-background border-t border-white/5 opacity-80 hover:opacity-100 transition-opacity mt-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-gutter px-gutter max-w-[1440px] mx-auto text-left">
          <div className="col-span-2 md:col-span-1">
            <span className="text-2xl font-black tracking-wider text-red-600 block mb-4">CINEVERSE</span>
            <p className="text-on-surface-variant text-sm max-w-xs">
              Experience the next generation of cinema streaming. Discover, watch, and share your favorite stories from across the globe.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <span className="font-bold text-on-background mb-1">Company</span>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/privacy/">Privacy Policy</a>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/terms/">Terms of Service</a>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/cookies/">Cookie Preferences</a>
          </div>
          <div className="flex flex-col gap-3">
            <span className="font-bold text-on-background mb-1">Support</span>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/help/">Help Center</a>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/contact/">Contact Us</a>
            <a className="text-on-surface-variant hover:text-primary-container transition-colors text-body-md font-body-md" href="/faq/">FAQ</a>
          </div>
          <div className="flex flex-col gap-3">
            <span className="font-bold text-on-background mb-1">Connect</span>
            <div className="flex gap-4">
              <a className="text-on-surface-variant hover:text-primary-container transition-colors" href="#">
                <span className="material-symbols-outlined">face_nod</span>
              </a>
              <a className="text-on-surface-variant hover:text-primary-container transition-colors" href="#">
                <span className="material-symbols-outlined">alternate_email</span>
              </a>
              <a className="text-on-surface-variant hover:text-primary-container transition-colors" href="#">
                <span className="material-symbols-outlined">play_circle</span>
              </a>
            </div>
          </div>
        </div>
        <div className="max-w-[1440px] mx-auto px-gutter mt-12 pt-8 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center text-xs text-on-surface-variant gap-4">
          <span>© 2026 CineVerse Global. All rights reserved.</span>
          <div className="flex gap-6">
            <span>English (US)</span>
            <span>Region: Global</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Layout;
