import { useState, useEffect, useRef } from 'react'

// Helper to extract YouTube Video ID
const getYouTubeId = (url) => {
  if (!url) return null;
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

function Watch({ payload, user, csrfToken }) {
  const { movie, history = {}, related_movies = [] } = payload;
  const initialProgress = history?.progress || 0;
  const ytId = getYouTubeId(movie.video_url);

  const videoRef = useRef(null);
  const progressContainerRef = useRef(null);
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(0.75);
  const [progressPercent, setProgressPercent] = useState(initialProgress);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [uiVisible, setUiVisible] = useState(true);
  
  const uiTimeoutRef = useRef(null);

  const syncProgress = (force = false) => {
    const video = videoRef.current;
    if (video && video.duration) {
      const progressPercentage = Math.round((video.currentTime / video.duration) * 100);
      
      if (force || (!video.paused)) {
        fetch('/api/watch/progress/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            movie_id: movie.id,
            progress: progressPercentage
          }),
          keepalive: true
        })
        .then(res => res.json())
        .then(data => {
          console.log("Progress synced percentage:", data.progress);
        })
        .catch(err => console.error(err));
      }
    }
  };

  // Auto-hide UI on inactivity
  const showUI = () => {
    setUiVisible(true);
    if (uiTimeoutRef.current) clearTimeout(uiTimeoutRef.current);
    if (isPlaying) {
      uiTimeoutRef.current = setTimeout(() => {
        setUiVisible(false);
      }, 5000);
    }
  };

  useEffect(() => {
    const handleMouseMove = () => showUI();
    const handleKeyDown = () => showUI();
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('keydown', handleKeyDown);
    
    // Initial trigger
    showUI();

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('keydown', handleKeyDown);
      if (uiTimeoutRef.current) clearTimeout(uiTimeoutRef.current);
    };
  }, [isPlaying]);

  // Set initial video progress when metadata is loaded
  const handleLoadedMetadata = () => {
    const video = videoRef.current;
    if (!video) return;
    setDuration(video.duration);
    if (initialProgress > 0 && initialProgress < 100) {
      video.currentTime = (initialProgress / 100) * video.duration;
    }
  };

  const handleTimeUpdate = () => {
    const video = videoRef.current;
    if (!video) return;
    setCurrentTime(video.currentTime);
    if (video.duration) {
      setProgressPercent((video.currentTime / video.duration) * 100);
    }
  };

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;
    if (video.paused) {
      video.play();
      setIsPlaying(true);
    } else {
      video.pause();
      setIsPlaying(false);
      syncProgress(true); // Sync immediately when pausing
    }
    showUI();
  };

  const handleSkip = (secs) => {
    const video = videoRef.current;
    if (!video) return;
    video.currentTime = Math.min(Math.max(video.currentTime + secs, 0), video.duration || 0);
    showUI();
  };

  const toggleMute = () => {
    const video = videoRef.current;
    if (!video) return;
    video.muted = !video.muted;
    setIsMuted(video.muted);
    showUI();
  };

  const handleVolumeChange = (val) => {
    const video = videoRef.current;
    if (!video) return;
    video.volume = val;
    setVolume(val);
    video.muted = (val === 0);
    setIsMuted(val === 0);
    showUI();
  };

  const handleProgressClick = (e) => {
    const video = videoRef.current;
    const progressContainer = progressContainerRef.current;
    if (!video || !progressContainer) return;
    const rect = progressContainer.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const percentage = clickX / rect.width;
    video.currentTime = percentage * video.duration;
    setCurrentTime(video.currentTime);
    setProgressPercent(percentage * 100);
    showUI();
    // Sync immediately on seek (using setTimeout to allow currentTime to settle)
    setTimeout(() => syncProgress(true), 50);
  };

  const toggleFullscreen = () => {
    const container = document.getElementById('videoContainer');
    if (!container) return;
    if (!document.fullscreenElement) {
      container.requestFullscreen().catch(err => console.error(err));
    } else {
      document.exitFullscreen();
    }
    showUI();
  };

  // Sync progress back to database every 5 seconds
  useEffect(() => {
    const syncInterval = setInterval(() => {
      syncProgress(false);
    }, 5000);

    return () => {
      clearInterval(syncInterval);
      syncProgress(true); // Sync immediately on unmount
    };
  }, [movie.id, csrfToken]);

  // Sync progress on window unload and visibility change (e.g. closing tab, navigating away)
  useEffect(() => {
    const handleUnloadOrHide = () => {
      syncProgress(true);
    };

    window.addEventListener('beforeunload', handleUnloadOrHide);
    
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        syncProgress(true);
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleUnloadOrHide);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [movie.id, csrfToken]);

  // Format time display
  const formatTime = (secs) => {
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = Math.floor(secs % 60);
    return `${h > 0 ? h + ':' : ''}${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
  };

  return (
    <main className="relative min-h-screen lg:h-screen w-screen bg-[#09090b] flex flex-col lg:flex-row pt-[132px] md:pt-20 text-left select-none overflow-y-auto lg:overflow-y-hidden custom-scrollbar">
      {/* Video Player layer */}
      <div className="relative w-full aspect-video lg:flex-grow lg:h-full lg:aspect-auto overflow-hidden bg-black" id="videoContainer">
        {ytId ? (
          <iframe 
            className="w-full h-full object-contain bg-black relative z-10"
            src={`https://www.youtube.com/embed/${ytId}?autoplay=1&rel=0`}
            title={movie.title}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <video 
            ref={videoRef}
            id="player"
            className="w-full h-full object-contain bg-black pointer-events-none"
            onLoadedMetadata={handleLoadedMetadata}
            onTimeUpdate={handleTimeUpdate}
            src={movie.video_url}
          />
        )}
        
        {/* Click-to-pause layer */}
        {!ytId && <div className="absolute inset-0 z-10 cursor-pointer" onClick={togglePlay}></div>}

        {!ytId && (
          <div className={`absolute inset-0 video-gradient-overlay pointer-events-none transition-opacity duration-500 ${uiVisible ? 'opacity-100' : 'opacity-0'}`}></div>
        )}

        {/* UI Info Overlay (Desktop only) */}
        {!ytId && (
          <div className={`hidden lg:block absolute bottom-36 left-4 right-4 sm:left-10 sm:right-auto sm:max-w-xl z-20 transition-all duration-500 transform ${
            uiVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0 pointer-events-none'
          }`} id="movie-info">
            <div className="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-4">
              <span className="bg-primary-container text-white text-[9px] sm:text-[10px] font-bold px-1.5 sm:px-2 py-0.5 rounded tracking-widest uppercase">CineVerse Theater</span>
              <span className="text-white/60 font-body-md text-xs sm:text-sm">{movie.release_year}</span>
              <span className="text-white/60 font-body-md text-xs sm:text-sm border border-white/20 px-1.5 rounded">{movie.language}</span>
            </div>
            <h1 className="text-2xl sm:text-4xl md:text-5xl lg:text-display-lg text-white mb-2 sm:mb-4 font-bold leading-tight sm:leading-none truncate sm:whitespace-normal">{movie.title}</h1>
            <p className="text-xs sm:text-sm md:text-body-md lg:text-body-lg text-white/80 mb-4 sm:mb-6 line-clamp-2">{movie.description}</p>
            <div className="flex gap-4">
              <a href={`/movies/${movie.id}/`} className="glass-panel px-4 py-2 sm:px-6 sm:py-3 rounded-xl flex items-center gap-2 hover:bg-white/10 transition-all text-white font-bold text-xs sm:text-sm">
                <span className="material-symbols-outlined text-sm sm:text-base">info</span>
                <span>Details</span>
              </a>
            </div>
          </div>
        )}

        {/* Playback Controls (Pinned Bottom) */}
        {!ytId && (
          <div className={`absolute bottom-0 left-0 right-0 z-30 px-4 sm:px-gutter pb-2 sm:pb-8 pt-4 sm:pt-12 bg-gradient-to-t from-black/95 via-black/80 to-transparent transition-all duration-500 transform ${
            uiVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0 pointer-events-none'
          }`} id="media-controls">
            {/* Progress Bar */}
            <div 
              ref={progressContainerRef}
              onClick={handleProgressClick}
              className="progress-container group relative w-full py-2 mb-2 sm:mb-4 cursor-pointer"
            >
              <div className="progress-track w-full bg-white/20 h-1.5 rounded-full overflow-hidden">
                <div className="h-full bg-primary-container relative" style={{ width: `${progressPercent}%` }}>
                  <div className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-primary-container rounded-full shadow-[0_0_15px_#e50914] scale-0 group-hover:scale-100 transition-transform"></div>
                </div>
              </div>
            </div>
            
            {/* Control buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-between sm:items-center">
              <div className="flex flex-wrap items-center gap-4 sm:gap-6 justify-between sm:justify-start">
                <div className="flex items-center gap-4 sm:gap-6">
                  <button onClick={togglePlay} className="text-white hover:text-primary-container transition-colors duration-300 flex items-center justify-center cursor-pointer">
                    <span className="material-symbols-outlined !text-2xl sm:!text-4xl" data-weight="fill">
                      {isPlaying ? 'pause' : 'play_arrow'}
                    </span>
                  </button>
                  <button onClick={() => handleSkip(-10)} className="text-white/70 hover:text-white transition-colors flex items-center justify-center cursor-pointer">
                    <span className="material-symbols-outlined !text-xl sm:!text-3xl">replay_10</span>
                  </button>
                  <button onClick={() => handleSkip(30)} className="text-white/70 hover:text-white transition-colors flex items-center justify-center cursor-pointer">
                    <span className="material-symbols-outlined !text-xl sm:!text-3xl">forward_30</span>
                  </button>
                </div>
                <div className="flex items-center gap-2 sm:gap-3">
                  <button onClick={toggleMute} className="text-white/70 hover:text-white transition-colors flex items-center justify-center cursor-pointer">
                    <span className="material-symbols-outlined text-white/70 text-sm sm:text-base">
                      {isMuted ? 'volume_off' : (volume > 0.5 ? 'volume_up' : 'volume_down')}
                    </span>
                  </button>
                  <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={volume}
                    onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
                    className="hidden sm:inline-block w-16 sm:w-24 accent-white bg-white/20 h-1 rounded-full appearance-none cursor-pointer"
                  />
                </div>
                <span className="text-xs sm:text-body-md text-white/80 tabular-nums">
                  {formatTime(currentTime)} / {formatTime(duration)}
                </span>
              </div>
              
              <div className="flex items-center justify-end gap-6">
                <button 
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="hidden lg:flex text-white/70 hover:text-white transition-colors flex items-center justify-center cursor-pointer"
                >
                  <span className="material-symbols-outlined !text-xl sm:!text-2xl">video_library</span>
                </button>
                <button onClick={toggleFullscreen} className="text-white/70 hover:text-white transition-colors flex items-center justify-center cursor-pointer">
                  <span className="material-symbols-outlined !text-2xl sm:!text-3xl">fullscreen</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Mobile Info & Recommendations Section (visible only on mobile) */}
      <div className="lg:hidden w-full px-6 py-8 text-left text-white bg-[#09090b] space-y-6 overflow-y-visible">
        {/* Title and metadata */}
        <div>
          <div className="flex items-center gap-3 mb-3">
            <span className="bg-primary-container text-white text-[10px] font-bold px-2 py-0.5 rounded tracking-widest uppercase">CineVerse Theater</span>
            <span className="text-white/60 text-sm">{movie.release_year}</span>
            <span className="text-white/60 text-sm border border-white/20 px-1.5 rounded">{movie.language}</span>
          </div>
          <h1 className="text-2xl font-bold mb-3 text-white uppercase tracking-tight">{movie.title}</h1>
          <p className="text-sm text-white/70 leading-relaxed font-body-md">{movie.description}</p>
        </div>

        {/* Action button */}
        <div className="flex gap-4">
          <a href={`/movies/${movie.id}/`} className="glass-panel px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-white/10 transition-all text-white font-bold text-xs">
            <span className="material-symbols-outlined text-sm">info</span>
            <span>Details & Info</span>
          </a>
        </div>

        {/* Up Next / Recommendations list */}
        <div className="pt-8 border-t border-white/10">
          <h2 className="font-headline-md text-headline-md mb-6 text-white">Up Next</h2>
          <div className="space-y-4">
            {related_movies.map(rel => (
              <div 
                key={rel.id} 
                onClick={() => window.location.href = `/movies/${rel.id}/watch/`}
                className="flex gap-4 cursor-pointer group"
              >
                <div className="relative w-32 aspect-video rounded-xl overflow-hidden flex-shrink-0">
                  <img 
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
                    src={rel.banner_url || rel.poster_url}
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = 'https://placehold.co/320x180?text=No+Preview';
                    }}
                  />
                  <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                    <span className="material-symbols-outlined text-2xl text-white">play_circle</span>
                  </div>
                </div>
                <div className="flex flex-col justify-center min-w-0">
                  <h3 className="font-bold text-white group-hover:text-primary-container transition-colors truncate text-sm">{rel.title}</h3>
                  <p className="text-xs text-on-surface-variant/70 mt-1">{rel.release_year} • {rel.duration}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommendations Sidebar (Desktop only) */}
      <aside className={`hidden lg:block sidebar-transition w-96 h-full glass-panel border-l border-white/10 z-40 fixed right-0 top-0 pt-16 md:relative overflow-y-auto custom-scrollbar transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0 lg:block'
      }`}>
        <div className="p-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="font-headline-md text-headline-md text-white">Up Next</h2>
            <button className="lg:hidden text-white" onClick={() => setSidebarOpen(false)}>
              <span className="material-symbols-outlined">close</span>
            </button>
          </div>
          <div className="space-y-6">
            {related_movies.map(rel => (
              <div 
                key={rel.id} 
                onClick={() => window.location.href = `/movies/${rel.id}/watch/`}
                className="group cursor-pointer text-left"
              >
                <div className="relative aspect-video rounded-xl overflow-hidden mb-3 ring-2 ring-transparent group-hover:ring-primary-container/50 transition-all">
                  <img 
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
                    src={rel.banner_url || rel.poster_url}
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = 'https://placehold.co/320x180?text=No+Preview';
                    }}
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                    <span className="material-symbols-outlined !text-4xl text-white">play_circle</span>
                  </div>
                </div>
                <h3 className="font-body-md font-bold text-white group-hover:text-primary-container transition-colors truncate">{rel.title}</h3>
                <p className="font-body-md text-sm text-on-surface-variant/70">{rel.release_year} • {rel.duration}</p>
              </div>
            ))}
          </div>
        </div>
      </aside>
    </main>
  );
}

export default Watch;
