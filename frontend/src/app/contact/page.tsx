import { Mail } from 'lucide-react';

export default function ContactPage() {
  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono mt-12 text-[var(--text-color)]">
      <div className="flex items-center gap-3 mb-8">
        <Mail className="w-8 h-8 text-[var(--main-color)]" />
        <h1 className="text-2xl font-bold">Contact</h1>
      </div>
      <p className="text-sm text-[var(--sub-color)] mb-4 leading-relaxed">
        If you encounter a bug, have a feature request or just want to say hi - here are the different ways you can contact us directly.
      </p>
      <div className="mt-8">
        <a href="mailto:support@typeforge.app" className="bg-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/20 text-[var(--main-color)] px-6 py-3 rounded-lg transition-colors inline-block">
          Email Us: support@typeforge.app
        </a>
      </div>
    </div>
  );
}
