import { useState, useEffect } from 'react'

function Login({ payload, csrfToken }) {
  const { error = '' } = payload;
  const [showPassword, setShowPassword] = useState(false);
  const [rotatePanel, setRotatePanel] = useState({ x: 0, y: 0 });

  // Mouse tracking rotation effect for premium aesthetics
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (window.innerWidth > 768) {
        const x = (e.clientX / window.innerWidth - 0.5) * 4;
        const y = (e.clientY / window.innerHeight - 0.5) * -4;
        setRotatePanel({ x, y });
      }
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="bg-[#0F1117] min-h-screen text-on-background font-body-md overflow-hidden relative flex flex-col justify-between">
      {/* Background Cinematic Collage */}
      <div className="absolute inset-0 z-0 overflow-hidden select-none pointer-events-none">
        <div 
          className="grid gap-3 opacity-30 w-[150vw] h-[150vh] transform -rotate-12 -translate-y-[15%] -translate-x-[10%]"
          style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))' }}
        >
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAM5IcsnMpWPK0fvkgb-JSIgA4ibf2aLRlo1l7DYVThoMd1M6KLGVJvS1LQlIUMKY8D-TKYcfSL3eeicmDdLUmlbaYDt_GqJOq9HtKrxQeJEnGAPo9kA9LP3xRaPb9brBJ5sKr9YYSJb6G1LyaBpPeA799eDqm1NiPmj2gvIIr-KsMhIcXR8gT5iT2zaDm8ms70nEnuuD6dkVDATq0vIBJpw3VKYVXOtEuvp-TKAiwIHhbdspuJRY8Wm1-kG46w1BsgJ1Xmw7PrzTJo" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDGe6sSvYm9I_MgUFj0zjykZ0lc9oMMj0wn-XkCoDQtiY3k_mLCvRt_5zvxPmY3YiKQEA5AFnP8iqGDRscbuC01izo0yJp7cSQDB0HSTTD7Eh7ydTz-GlRWEbcStsVg943doa-oU3XmWzBcmheCSO4rsVM80GJFAo0IfljyHjF2pwNMJo99YLC32-VAsjmjmfnV7i7fuzDuApotB6UKgAJ023Tfek_AcAZ0GnRhTDegEdsRAXa7bCGW32WyQGWTTc2kGyFqY6h_d6BX" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBof7-xqIxcroA4StW9hEJaCFE24ShKJzLuX4PDf3xgMdBCpciNg1N9fJSjA-_PHdpY6wwQltKPNzPlEZavTMYPJJbfeK2LtbcqeJMr_IteXQJOBa8wL1uRPq-OdhK80Hs6zI0qdpXInFzrMQe-bgeA2pi77PIcRfigzImYq1ubt2CL2val5F3-fwMeo_6oGtNixyI8tNFY6G9M7Bhu4woXnYDJZbLYXJfVERq3suXTTPqsOp7kmOpJ4sKr-9s4rh1KEcBIYH5AZA6d" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDpuyMIEGgtsGkc9brzZCLvx2wUQjIqWldt67PyZ2C4orGETrr1N3IrRB4tkVXeDh8uD-qVoMabUfdsWfbfkN16McEPWovCqAMPQJq2ob1OGA9-ou4ql6_meo-dt4sDJgUeB3DS6-yVo2Xmdt6X8YUTjV9NVaxW358jQLy5Oe-pqwnju6rzuYzwTZt7bCcegBQg7PfS3l_G_NBbX4Dj2yTJdreN-j9UbLI8IcOvL1Yn5HW0HYeUbpybTBchtIiiTdxb3YejGPy-hbX2" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDBTNhfpWDCt_-SgAgsXJgb5n4J6NLGPnNaTsmiCcdDmNeWvlOuEZNln9_o9s4m_PboaUXX3QWdenTWPgxfgOu1opS28j03Bcu6tSzS4dk5jPuL9nmjCySZ4iLdUMaxeZBF0oLIkoYKJYd6CF4ihFFx6aQH8gm6u3IZ0l1yH8hSB0_HL4QwSsqHKLvr5uaXeb1L3IeStcNo5s0QPTCgYZhyxsRrrxpQWPBGFT33MoTFzjDb-HPvUsX6lyr900_KvOl6VQ50YvyqrTdo" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAyUYirHt0ujR0VyNad6ERtFDoct8gdHcS2AhchzLhaNUKh_sdtIiXxX1H3uY46hEhZM2l5YYvgD6yDVTSzgtFss666-VwgXX37EXd36AdybqEuAeXlUBMKl_dTHNb0p3fxYNWQJ-4PCgyzwUR1JHQYF5DCkqD7MnFKTwfop3JCRCPN9x5ZQy6mQGcNO4StLqGgjt3sS3uL34V2VcKqhgXoecvPyNMZw_UpcXRIF02Cc0ugl8vnofeCc91nf3f1mZfC_iWDLb59ga0M" alt=""/>
        </div>
        <div className="absolute inset-0 bg-[#0F1117]/85" style={{ background: 'radial-gradient(circle, transparent 20%, #0F1117 100%)' }}></div>
      </div>

      <main className="relative z-10 min-h-screen flex flex-col items-center justify-center px-gutter py-8 text-left">
        <header className="mb-12 text-center">
          <a href="/" className="font-headline-lg text-headline-lg text-primary-container font-bold tracking-tight hover:brightness-110">CineVerse</a>
        </header>

        {/* Glassmorphism Login Card */}
        <section 
          className="glass-panel w-full max-w-[440px] p-8 md:p-10 rounded-xl shadow-2xl transition-transform duration-100 ease-out"
          style={{ transform: `perspective(1000px) rotateY(${rotatePanel.x}deg) rotateX(${rotatePanel.y}deg)` }}
        >
          <h2 className="font-headline-md text-headline-md text-white mb-8">Sign In</h2>
          
          {error && (
            <div className="mb-6 p-4 bg-error-container/20 border border-error-container/30 rounded-xl flex items-center gap-3 text-error text-sm font-semibold">
              <span className="material-symbols-outlined text-[20px] text-error">error</span>
              <span>{error}</span>
            </div>
          )}

          <form method="POST" action="/login/" className="space-y-6">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            
            <div className="space-y-2">
              <label className="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest" htmlFor="username">Username</label>
              <input 
                className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-3 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                id="username" 
                name="username" 
                placeholder="marcus" 
                required 
                type="text"
              />
            </div>

            <div className="space-y-2">
              <label className="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest" htmlFor="password">Password</label>
              <div className="relative">
                <input 
                  className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-3 pr-10 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                  id="password" 
                  name="password" 
                  placeholder="••••••••" 
                  required 
                  type={showPassword ? 'text' : 'password'}
                />
                <button 
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-0 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer" 
                  type="button"
                >
                  <span className="material-symbols-outlined text-[20px]">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center space-x-2 cursor-pointer group">
                <input type="checkbox" className="rounded bg-[#1A1D29] border-outline-variant text-primary-container focus:ring-0 cursor-pointer w-4 h-4" />
                <span className="text-body-md text-on-surface-variant group-hover:text-on-surface transition-colors">Remember me</span>
              </label>
              <a className="text-body-md text-on-surface-variant hover:text-white transition-colors" href="#">Forgot password?</a>
            </div>

            <button className="w-full bg-primary-container hover:bg-[#ff1f2d] text-white font-bold py-4 rounded transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-primary-container/20 cursor-pointer" type="submit">
              Sign In
            </button>
          </form>
          
          <div className="mt-8 pt-6 border-t border-white/5 space-y-6">
            <p className="text-center text-on-surface-variant text-body-md">
              New to CineVerse? 
              <a className="text-white font-bold hover:text-primary-container transition-colors ml-1" href="/register/">Create Account</a>
            </p>
          </div>
        </section>

        <footer className="mt-12 opacity-50 flex flex-wrap justify-center gap-6">
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Terms of Use</a>
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Privacy Policy</a>
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Cookie Preferences</a>
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Help Center</a>
        </footer>
      </main>
    </div>
  )
}

export default Login;
