import { useState } from 'react'

function Subscription({ payload, csrfToken }) {
  const { profile = {}, success_message = '' } = payload;
  const currentPlan = profile.subscription_plan || 'Basic';

  return (
    <main className="pt-32 pb-section-gap px-gutter max-w-[1440px] mx-auto text-left select-none">
      {/* Header Section */}
      <header className="text-center mb-16 space-y-4">
        <h1 className="font-display-lg text-3xl sm:text-5xl md:text-display-lg text-on-background max-w-3xl mx-auto text-white leading-tight">
          Choose the perfect plan for your <span className="text-primary-container">cinema journey.</span>
        </h1>
        <p className="font-body-lg text-base sm:text-body-lg text-on-surface-variant max-w-2xl mx-auto">
          Stream unlimited movies and TV shows on your phone, tablet, laptop, and TV without paying more.
        </p>
      </header>

      {success_message && (
        <div className="mb-8 p-4 bg-green-600/20 border border-green-600/30 rounded-xl flex items-center gap-3 text-green-400 text-sm font-semibold max-w-3xl mx-auto text-center justify-center">
          <span className="material-symbols-outlined text-base">check_circle</span>
          <span>{success_message}</span>
        </div>
      )}

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-24 items-end">
        {/* Basic Plan */}
        <div className={`glass-panel p-6 sm:p-8 rounded-xl flex flex-col h-full transition-transform duration-300 hover:scale-[1.02] ${
          currentPlan === 'Basic' ? 'border-primary-container/50 shadow-[0_0_40px_rgba(229,9,20,0.15)]' : ''
        }`}>
          <div className="mb-8">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-2 block">ENTRY LEVEL</span>
            <h3 className="font-headline-md text-headline-md text-white text-xl font-bold">Basic</h3>
          </div>
          <div className="mb-8">
            <span className="font-headline-lg text-headline-lg text-white text-3xl font-extrabold">₹199</span>
            <span className="text-on-surface-variant text-sm">/month</span>
          </div>
          <ul className="space-y-4 mb-10 flex-grow">
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">720p (HD) Streaming</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">1 Simultaneous Screen</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">Mobile &amp; Tablet Access</span>
            </li>
          </ul>
          <form method="POST" action="/subscription/">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            <input type="hidden" name="subscription_plan" value="Basic"/>
            <button type="submit" className={`w-full py-4 rounded-lg font-bold transition-all cursor-pointer ${
              currentPlan === 'Basic' ? 'bg-primary-container text-white' : 'bg-white/5 border border-white/10 hover:bg-white/10 text-white'
            }`}>
              {currentPlan === 'Basic' ? 'Current Plan' : 'Choose Plan'}
            </button>
          </form>
        </div>

        {/* Premium Plan (Highlighted) */}
        <div className="glass-panel shadow-[0_0_50px_rgba(229,9,20,0.15)] p-6 sm:p-10 rounded-xl flex flex-col h-full relative border-primary-container/30 md:scale-105 z-10 overflow-hidden">
          <div className="absolute top-0 right-0 bg-primary-container text-white px-6 py-2 rounded-bl-xl font-label-caps text-label-caps text-xs font-bold uppercase tracking-wider">MOST POPULAR</div>
          <div className="mb-8">
            <span className="font-label-caps text-label-caps text-primary-container mb-2 block">ULTIMATE CINEMA</span>
            <h3 className="font-headline-md text-headline-md text-white text-xl font-bold">Premium</h3>
          </div>
          <div className="mb-8">
            <span className="font-headline-lg text-headline-lg text-white text-3xl font-extrabold">₹649</span>
            <span className="text-on-surface-variant text-sm">/month</span>
          </div>
          <ul className="space-y-4 mb-10 flex-grow">
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-white font-medium text-sm">4K + HDR (Ultra HD)</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-white font-medium text-sm">4 Simultaneous Screens</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-white font-medium text-sm">Dolby Atmos Audio</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-white font-medium text-sm">Unlimited Offline Downloads</span>
            </li>
          </ul>
          <form method="POST" action="/subscription/">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            <input type="hidden" name="subscription_plan" value="Premium"/>
            <button type="submit" className={`w-full py-4 rounded-lg font-bold transition-all cursor-pointer ${
              currentPlan === 'Premium' ? 'bg-primary-container text-on-primary-container' : 'bg-white/5 border border-white/10 hover:bg-white/10 text-white'
            }`}>
              {currentPlan === 'Premium' ? 'Current Plan' : 'Choose Plan'}
            </button>
          </form>
        </div>

        {/* Standard Plan */}
        <div className={`glass-panel p-6 sm:p-8 rounded-xl flex flex-col h-full transition-transform duration-300 hover:scale-[1.02] ${
          currentPlan === 'Standard' ? 'border-primary-container/50 shadow-[0_0_40px_rgba(229,9,20,0.15)]' : ''
        }`}>
          <div className="mb-8">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-2 block">BEST VALUE</span>
            <h3 className="font-headline-md text-headline-md text-white text-xl font-bold">Standard</h3>
          </div>
          <div className="mb-8">
            <span className="font-headline-lg text-headline-lg text-white text-3xl font-extrabold">₹499</span>
            <span className="text-on-surface-variant text-sm">/month</span>
          </div>
          <ul className="space-y-4 mb-10 flex-grow">
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">1080p (Full HD) Streaming</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">2 Simultaneous Screens</span>
            </li>
            <li className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary-container text-[20px]">check_circle</span>
              <span className="text-on-surface-variant text-sm">All Devices Supported</span>
            </li>
          </ul>
          <form method="POST" action="/subscription/">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
            <input type="hidden" name="subscription_plan" value="Standard"/>
            <button type="submit" className={`w-full py-4 rounded-lg font-bold transition-all cursor-pointer ${
              currentPlan === 'Standard' ? 'bg-primary-container text-white' : 'bg-white/5 border border-white/10 hover:bg-white/10 text-white'
            }`}>
              {currentPlan === 'Standard' ? 'Current Plan' : 'Choose Plan'}
            </button>
          </form>
        </div>
      </div>

      {/* Comparison Table Section */}
      <section className="mt-section-gap">
        <h2 className="font-headline-lg text-headline-lg text-on-background text-center mb-12 text-white">
          Compare our <span className="text-primary-container">features</span>
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/10">
                <th className="py-4 md:py-6 font-headline-md text-white w-1/3 text-sm sm:text-lg font-bold">Features</th>
                <th className="py-4 md:py-6 font-headline-md text-center text-on-surface-variant text-xs sm:text-base font-bold">Basic</th>
                <th className="py-4 md:py-6 font-headline-md text-center text-on-surface-variant text-xs sm:text-base font-bold">Standard</th>
                <th className="py-4 md:py-6 font-headline-md text-center text-primary-container text-xs sm:text-base font-bold">Premium</th>
              </tr>
            </thead>
            <tbody className="font-body-md text-xs sm:text-sm md:text-body-md">
              <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td class="py-4 md:py-6 text-white font-medium">Monthly Price</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">₹199</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">₹499</td>
                <td class="py-4 md:py-6 text-center text-white font-bold">₹649</td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td class="py-4 md:py-6 text-white font-medium">Video Quality</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">Good (720p)</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">Better (1080p)</td>
                <td class="py-4 md:py-6 text-center text-white font-bold">Best (4K+HDR)</td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td class="py-4 md:py-6 text-white font-medium">Concurrent Screens</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">1</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">2</td>
                <td class="py-4 md:py-6 text-center text-white font-bold">4</td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td class="py-4 md:py-6 text-white font-medium">Ad-Free Viewing</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">
                  <span className="material-symbols-outlined text-primary-container text-sm sm:text-base">check</span>
                </td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">
                  <span className="material-symbols-outlined text-primary-container text-sm sm:text-base">check</span>
                </td>
                <td class="py-4 md:py-6 text-center text-white">
                  <span className="material-symbols-outlined text-primary-container text-sm sm:text-base" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                </td>
              </tr>
              <tr className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td class="py-4 md:py-6 text-white font-medium">Device Downloads</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">—</td>
                <td class="py-4 md:py-6 text-center text-on-surface-variant">
                  <span className="material-symbols-outlined text-primary-container text-sm sm:text-base">check</span>
                </td>
                <td class="py-4 md:py-6 text-center text-white">
                  <span className="material-symbols-outlined text-primary-container text-sm sm:text-base" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* CTA Section */}
      <section className="mt-section-gap relative h-[320px] sm:h-[400px] rounded-2xl overflow-hidden flex items-center justify-center text-center px-6 sm:px-10">
        <img 
          className="absolute inset-0 w-full h-full object-cover opacity-40 grayscale hover:grayscale-0 transition-all duration-700" 
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuBvi4hiO5WazJ1KEE19neveRyl3p5KdDgPSi04nkP5VG2s0ce_E72cubKXiieqyh-M9X2StdkouxqsXRccSM3jeyHN3G_j8jeWm71tw0E8B0eSe9xRGQYGbZdcWc1lddQ3-V-fP0wP0vmq2e-q4U_vcIvNUAv8v9Pj6yze_WrCybpqTKmGphh9VjqPVF0rnfQpdkcUsdbIFlXChRJiBF1ZFr8IPJBBqISUFmObSUXX3dx3-IW_DOASuuiWTKZTWDgwZIHCJ4C7JEszm"
          alt="CTA background"
        />
        <div className="relative z-10 max-w-2xl">
          <h2 className="font-headline-lg text-2xl sm:text-3xl md:text-headline-lg text-white mb-6 font-bold leading-tight">Ready to start watching?</h2>
          <p className="text-sm sm:text-body-lg text-on-surface-variant mb-6 sm:mb-10">Join millions of cinephiles and experience cinema like never before. No commitments, cancel anytime.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/" className="px-6 py-3 sm:px-8 sm:py-4 bg-primary-container text-on-primary-container rounded-lg font-bold text-sm sm:text-lg transition-transform hover:scale-105 flex items-center justify-center">Get Started Now</a>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Subscription;
