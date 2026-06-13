import { Heart } from 'lucide-react';

export default function SupportPage() {
  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono mt-12 text-[var(--text-color)]">
      <div className="flex items-center gap-3 mb-8">
        <Heart className="w-8 h-8 text-[var(--main-color)]" />
        <h1 className="text-2xl font-bold">Support Us</h1>
      </div>
      <p className="text-sm text-[var(--sub-color)] mb-4 leading-relaxed">
        Thanks to everyone who has supported this project. It would not be possible without you and your continued support.
      </p>
      <div className="mt-8 space-y-4">
        <div className="bg-[var(--sub-color)]/10 p-6 rounded-xl border border-[var(--sub-color)]/20">
          <h2 className="text-lg font-bold text-[var(--main-color)] mb-2">Donate</h2>
          <p className="text-sm text-[var(--sub-color)] mb-4">Help keep the servers running by becoming a supporter.</p>
          <button className="bg-[var(--main-color)] text-[var(--bg-color)] px-4 py-2 rounded font-bold">Support via Patreon</button>
        </div>
      </div>
    </div>
  );
}
