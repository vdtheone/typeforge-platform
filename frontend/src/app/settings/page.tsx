'use client';

import { Settings as SettingsIcon } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono mt-8">
      <div className="flex items-center gap-3 mb-12 text-[var(--text-color)]">
        <SettingsIcon className="w-8 h-8 text-[var(--main-color)]" />
        <div>
          <h1 className="text-2xl font-bold">Settings</h1>
          <p className="text-sm text-[var(--sub-color)]">Configure your typing experience</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 text-[var(--text-color)]">
        <section>
          <h2 className="text-xl font-bold mb-6 text-[var(--main-color)]">behavior</h2>
          <div className="space-y-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold mb-1">quick restart</h3>
                <p className="text-xs text-[var(--sub-color)] leading-relaxed max-w-sm">Press tab, esc or enter to quickly restart the test. Using the "esc" option will move opening the commandline to the tab key.</p>
              </div>
              <div className="flex gap-2">
                <button className="bg-[var(--main-color)] text-[var(--bg-color)] px-3 py-1 rounded text-sm font-bold">esc</button>
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">tab</button>
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">enter</button>
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">off</button>
              </div>
            </div>

            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold mb-1">blind mode</h3>
                <p className="text-xs text-[var(--sub-color)] leading-relaxed max-w-sm">No errors or incorrect words are highlighted. Helps you to focus on raw speed.</p>
              </div>
              <div className="flex gap-2">
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">on</button>
                <button className="bg-[var(--main-color)] text-[var(--bg-color)] px-3 py-1 rounded text-sm font-bold">off</button>
              </div>
            </div>
            
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold mb-1">language</h3>
                <p className="text-xs text-[var(--sub-color)] leading-relaxed max-w-sm">Change in which language you want to type.</p>
              </div>
              <div className="flex gap-2">
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">english</button>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-xl font-bold mb-6 text-[var(--main-color)]">appearance</h2>
          <div className="space-y-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold mb-1">smooth caret</h3>
                <p className="text-xs text-[var(--sub-color)] leading-relaxed max-w-sm">The caret will move smoothly between letters and words.</p>
              </div>
              <div className="flex gap-2">
                <button className="bg-[var(--main-color)] text-[var(--bg-color)] px-3 py-1 rounded text-sm font-bold">on</button>
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">off</button>
              </div>
            </div>
            
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold mb-1">caret style</h3>
                <p className="text-xs text-[var(--sub-color)] leading-relaxed max-w-sm">Change the style of the caret during the test.</p>
              </div>
              <div className="flex gap-2">
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">_</button>
                <button className="bg-[var(--main-color)] text-[var(--bg-color)] px-3 py-1 rounded text-sm font-bold">|</button>
                <button className="bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/30 transition-colors px-3 py-1 rounded text-sm font-bold">block</button>
              </div>
            </div>
          </div>
        </section>
      </div>
      
      <div className="text-center mt-24 text-xs text-[var(--sub-color)]">
        More settings coming soon via backend user preferences API.
      </div>
    </div>
  );
}
