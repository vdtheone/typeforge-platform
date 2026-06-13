'use client';

import { Keyboard, Crown, Info, Settings, Bell, User as UserIcon, LogOut } from 'lucide-react';
import Link from 'next/link';
import { ThemeSwitcher } from './ThemeSwitcher';
import { useAuthStore } from '@/utils/api';
import { useState } from 'react';
import NotificationSidebar from '@/components/notifications/NotificationSidebar';

export default function Header() {
  const [isNotifOpen, setIsNotifOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuthStore();
  return (
    <header className="w-full flex items-center justify-between py-8">
      {/* Left side: Logo & Nav Icons */}
      <div className="flex items-center gap-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="text-[var(--main-color)] transition-all duration-300 group-hover:scale-110">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="M6 8h.001"/><path d="M10 8h.001"/><path d="M14 8h.001"/><path d="M18 8h.001"/><path d="M8 12h.001"/><path d="M12 12h.001"/><path d="M16 12h.001"/><path d="M7 16h10"/></svg>
          </div>
          <div className="flex flex-col mt-1">
            <span className="text-[10px] text-[var(--sub-color)] font-mono leading-none -mb-1 ml-0.5 opacity-70">forge your</span>
            <h1 className="text-3xl font-bold tracking-tight leading-none text-[var(--text-color)] group-hover:text-[var(--main-color)] transition-colors duration-300">
              typeforge
            </h1>
          </div>
        </Link>

        {/* Primary Nav Icons */}
        <nav className="hidden md:flex items-center gap-5 text-[var(--sub-color)] ml-4 mt-2">
          <Link href="/" className="hover:text-[var(--text-color)] transition-colors">
            <Keyboard className="w-5 h-5" />
          </Link>
          <Link href="/leaderboards" className="hover:text-[var(--text-color)] transition-colors">
            <Crown className="w-5 h-5" />
          </Link>
          <Link href="/about" className="hover:text-[var(--text-color)] transition-colors">
            <Info className="w-5 h-5" />
          </Link>
          <Link href="/settings" className="hover:text-[var(--text-color)] transition-colors">
            <Settings className="w-5 h-5" />
          </Link>
        </nav>
      </div>

      {/* Right side: User & Theme */}
      <div className="flex items-center gap-5 text-[var(--sub-color)] mt-2">
        <button onClick={() => setIsNotifOpen(true)} className="hover:text-[var(--text-color)] transition-colors focus:outline-none">
          <Bell className="w-5 h-5" />
        </button>
        {isAuthenticated && user ? (
          <div className="flex items-center gap-3">
            <Link href="/account" className="text-sm font-mono text-[var(--main-color)] hover:underline">{user.username}</Link>
            <button onClick={logout} className="hover:text-[var(--error-color)] transition-colors" title="Log out">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <Link href="/login" className="hover:text-[var(--text-color)] transition-colors">
            <UserIcon className="w-5 h-5" />
          </Link>
        )}
        <div className="-mt-2">
          <ThemeSwitcher />
        </div>
      </div>
      
      <NotificationSidebar isOpen={isNotifOpen} onClose={() => setIsNotifOpen(false)} />
    </header>
  );
}
