import Link from 'next/link';
import { Mail, Heart, Code, MessageCircle, Shield, FileText, Palette, GitBranch } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full flex flex-col md:flex-row items-center justify-between py-6 text-[11px] font-mono text-[var(--sub-color)]">
      {/* Left side: Links */}
      <div className="flex flex-wrap items-center justify-center gap-4 mb-4 md:mb-0">
        <Link href="/contact" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <Mail className="w-3.5 h-3.5" /> contact
        </Link>
        <Link href="/support" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <Heart className="w-3.5 h-3.5" /> support
        </Link>
        <a href="https://github.com" target="_blank" rel="noreferrer" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <Code className="w-3.5 h-3.5" /> github
        </a>
        <a href="https://discord.com" target="_blank" rel="noreferrer" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <MessageCircle className="w-3.5 h-3.5" /> discord
        </a>

        <Link href="/terms" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <FileText className="w-3.5 h-3.5" /> terms
        </Link>
        <Link href="/privacy" className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors">
          <Shield className="w-3.5 h-3.5" /> privacy
        </Link>
      </div>

      {/* Right side: Indicators */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors cursor-pointer" title="Current Theme">
          <Palette className="w-3.5 h-3.5" /> typeforge dark
        </div>
        <div className="flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors cursor-pointer" title="Version">
          <GitBranch className="w-3.5 h-3.5" /> v1.0.0
        </div>
      </div>
    </footer>
  );
}
