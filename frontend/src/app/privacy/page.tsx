import { Shield } from 'lucide-react';

export default function PrivacyPage() {
  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono mt-12 text-[var(--text-color)]">
      <div className="flex items-center gap-3 mb-8">
        <Shield className="w-8 h-8 text-[var(--main-color)]" />
        <h1 className="text-2xl font-bold">Privacy Policy</h1>
      </div>
      <div className="text-sm text-[var(--sub-color)] space-y-6 leading-relaxed max-w-3xl">
        <section>
          <h2 className="text-lg font-bold text-[var(--text-color)] mb-2">Data Collection</h2>
          <p>We collect basic account information (email, username) and typing statistics. We do not sell your personal data to third parties.</p>
        </section>
        <section>
          <h2 className="text-lg font-bold text-[var(--text-color)] mb-2">Cookies</h2>
          <p>We use local storage and standard cookies to keep you logged in and persist your typing preferences (like theme, font, and caret style) across sessions.</p>
        </section>
      </div>
    </div>
  );
}
