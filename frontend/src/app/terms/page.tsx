import { FileText } from 'lucide-react';

export default function TermsPage() {
  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono mt-12 text-[var(--text-color)]">
      <div className="flex items-center gap-3 mb-8">
        <FileText className="w-8 h-8 text-[var(--main-color)]" />
        <h1 className="text-2xl font-bold">Terms of Service</h1>
      </div>
      <div className="text-sm text-[var(--sub-color)] space-y-6 leading-relaxed max-w-3xl">
        <p>By using TypeForge, you agree to these terms.</p>
        <section>
          <h2 className="text-lg font-bold text-[var(--text-color)] mb-2">1. Usage</h2>
          <p>Please do not use bots or automated scripts to interact with the typing engine or submit fraudulent scores to the leaderboards. We reserve the right to ban accounts violating this.</p>
        </section>
        <section>
          <h2 className="text-lg font-bold text-[var(--text-color)] mb-2">2. Accounts</h2>
          <p>You are responsible for keeping your password secure. We cannot and will not be liable for any loss or damage from your failure to maintain the security of your account and password.</p>
        </section>
      </div>
    </div>
  );
}
