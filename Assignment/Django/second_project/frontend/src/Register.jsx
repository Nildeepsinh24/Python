import { useState, useEffect } from 'react'

function Register({ payload, csrfToken }) {
  const { error = '' } = payload;
  const [showPassword, setShowPassword] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState('Basic');
  const [rotatePanel, setRotatePanel] = useState({ x: 0, y: 0 });

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
    <div className="bg-[#0F1117] min-h-screen text-on-background font-body-md overflow-x-hidden relative flex flex-col justify-between py-12">
      {/* Background Cinematic Collage */}
      <div className="absolute inset-0 z-0 overflow-hidden select-none pointer-events-none">
        <div 
          className="grid gap-3 opacity-30 w-[150vw] h-[150vh] transform -rotate-12 -translate-y-[15%] -translate-x-[10%]"
          style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))' }}
        >
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAM5IcsnMpWPK0fvkgb-JSIgA4ibf2aLRlo1l7DYVThoMd1M6KLGVJvS1LQlIUMKY8D-TKYcfSL3eeicmDdLUmlbaYDt_GqJOq9HtKrxQeJEnGAPo9kA9LP3xRaPb9brBJ5sKr9YYSJb6G1LyaBpPeA799eDqm1NiPmj2gvIIr-KsMhIcXR8gT5iT2zaDm8ms70nEnuuD6dkVDATq0vIBJpw3VKYVXOtEuvp-TKAiwIHhbdspuJRY8Wm1-kG46w1BsgJ1Xmw7PrzTJo" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDGe6sSvYm9I_MgUFj0zjykZ0lc9oMMj0wn-XkCoDQtiY3k_mLCvRt_5zvxPmY3YiKQEA5AFnP8iqGDRscbuC01izo0yJp7cSQDB0HSTTD7Eh7ydTz-GlRWEbcStsVg943doa-oU3XmWzBcmheCSO4rsVM80GJFAo0IfljyHjF2pwNMJo99YLC32-VAsjmjmfnV7i7fuzDuApotB6UKgAJ023Tfek_AcAZ0GnRhTDegEdsRAXa7bCGW32WyQGWTTc2kGyFqY6h_d6BX" alt=""/>
          <img className="w-full aspect-[2/3] object-cover rounded-lg" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBof7-xqIxcroA4StW9hEJaCFE24ShKJzLuX4PDf3xgMdBCpciNg1N9fJSjA-_PHdpY6wwQltKPNzPlEZavTMYPJJbfeK2LtbcqeJMr_IteXQJOBa8wL1uRPq-OdhK80Hs6zI0qdpXInFzrMQe-bgeA2pi77PIcRfigzImYq1ubt2CL2val5F3-fwMeo_6oGtNixyI8tNFY6G9M7Bhu4woXnYDJZbLYXJfVERq3suXTTPqsOp7kmOpJ4sKr-9s4rh1KEcBIYH5AZA6d" alt=""/>
        </div>
        <div className="absolute inset-0 bg-[#0F1117]/85" style={{ background: 'radial-gradient(circle, transparent 20%, #0F1117 100%)' }}></div>
      </div>

      <main className="relative z-10 flex flex-col items-center justify-center px-gutter text-left">
        <header className="mb-8 text-center">
          <a href="/" className="font-headline-lg text-headline-lg text-primary-container font-bold tracking-tight hover:brightness-110">CineVerse</a>
        </header>

        {/* Glassmorphism Register Card */}
        <section 
          className="glass-panel w-full max-w-[500px] p-8 md:p-10 rounded-xl shadow-2xl transition-transform duration-100 ease-out"
          style={{ transform: `perspective(1000px) rotateY(${rotatePanel.x}deg) rotateX(${rotatePanel.y}deg)` }}
        >
          <h2 className="font-headline-md text-headline-md text-white mb-6">Create Account</h2>
          
          {error && (
            <div className="mb-6 p-4 bg-error-container/20 border border-error-container/30 rounded-xl flex items-center gap-3 text-error text-sm font-semibold">
              <span className="material-symbols-outlined text-[20px] text-error">error</span>
              <span>{error}</span>
            </div>
          )}

          <form method="POST" action="/register/" className="space-y-4">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-widest" htmlFor="username">Username</label>
                <input 
                  className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-2.5 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                  id="username" 
                  name="username" 
                  placeholder="marcus" 
                  required 
                  type="text"
                />
              </div>

              <div className="space-y-1">
                <label className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-widest" htmlFor="email">Email</label>
                <input 
                  className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-2.5 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                  id="email" 
                  name="email" 
                  placeholder="marcus@example.com" 
                  required 
                  type="email"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-widest" htmlFor="password">Password</label>
                <input 
                  className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-2.5 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                  id="password" 
                  name="password" 
                  placeholder="••••••••" 
                  required 
                  type={showPassword ? 'text' : 'password'}
                />
              </div>

              <div className="space-y-1">
                <label className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-widest" htmlFor="confirm_password">Confirm Password</label>
                <input 
                  className="w-full bg-[#1A1D29] border-0 border-b-2 border-outline-variant focus:border-primary-container focus:ring-0 text-white py-2.5 transition-colors duration-300 placeholder-white/20 focus:outline-none" 
                  id="confirm_password" 
                  name="confirm_password" 
                  placeholder="••••••••" 
                  required 
                  type={showPassword ? 'text' : 'password'}
                />
              </div>
            </div>

            <div className="flex items-center justify-between text-xs py-1">
              <button 
                onClick={() => setShowPassword(!showPassword)}
                className="text-on-surface-variant hover:text-white transition-colors cursor-pointer flex items-center gap-1" 
                type="button"
              >
                <span className="material-symbols-outlined text-[16px]">
                  {showPassword ? 'visibility_off' : 'visibility'}
                </span>
                <span>{showPassword ? 'Hide Passwords' : 'Show Passwords'}</span>
              </button>
            </div>

            {/* Choose Subscription Tiers directly on Registration */}
            <div className="space-y-2 pt-2 border-t border-white/5">
              <label className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-widest block">Choose Subscription Plan</label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { name: 'Basic', price: '₹199/mo' }, 
                  { name: 'Standard', price: '₹499/mo' }, 
                  { name: 'Premium', price: '₹649/mo' }
                ].map(plan => (
                  <button
                    key={plan.name}
                    type="button"
                    onClick={() => setSelectedPlan(plan.name)}
                    className={`py-2 px-1 rounded-lg flex flex-col items-center justify-center gap-0.5 transition-all border cursor-pointer ${
                      selectedPlan === plan.name 
                        ? 'bg-primary-container text-white border-primary-container shadow' 
                        : 'bg-white/5 border-white/10 text-white hover:bg-white/10'
                    }`}
                  >
                    <span className="text-xs font-bold">{plan.name}</span>
                    <span className={`text-[10px] ${selectedPlan === plan.name ? 'text-white/90' : 'text-on-surface-variant'}`}>{plan.price}</span>
                  </button>
                ))}
              </div>
              <input type="hidden" name="subscription_plan" value={selectedPlan} />
            </div>

            <button className="w-full bg-primary-container hover:bg-[#ff1f2d] text-white font-bold py-4 rounded transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-primary-container/20 cursor-pointer mt-6" type="submit">
              Register Account
            </button>
          </form>

          <div className="mt-6 pt-4 border-t border-white/5 text-center">
            <p className="text-on-surface-variant text-body-md">
              Already have an account? 
              <a className="text-white font-bold hover:text-primary-container transition-colors ml-1" href="/login/">Sign In</a>
            </p>
          </div>
        </section>

        <footer className="mt-8 opacity-50 flex flex-wrap justify-center gap-6">
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Terms of Use</a>
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Privacy Policy</a>
          <a className="text-label-caps font-label-caps hover:text-primary-container transition-colors" href="#">Cookie Preferences</a>
        </footer>
      </main>
    </div>
  )
}

export default Register;
