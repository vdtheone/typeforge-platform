'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { Inbox, Megaphone, Bell, X } from 'lucide-react';

interface NotificationSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function NotificationSidebar({ isOpen, onClose }: NotificationSidebarProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
          />
          
          {/* Sidebar */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed top-0 right-0 h-full w-80 max-w-[85vw] bg-[var(--bg-color)] border-l border-[var(--sub-color)]/20 shadow-2xl z-50 flex flex-col font-mono text-[var(--sub-color)]"
          >
            <div className="flex justify-between items-center p-4 border-b border-[var(--sub-color)]/20">
              <span className="font-bold text-[var(--text-color)]">updates</span>
              <button onClick={onClose} className="hover:text-[var(--main-color)] transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-8">
              {/* Inbox Section */}
              <section>
                <div className="flex items-center justify-between text-sm mb-4">
                  <div className="flex items-center gap-2">
                    <Inbox className="w-4 h-4" />
                    <span className="font-bold">Inbox</span>
                  </div>
                  <span className="text-xs text-[var(--error-color)]">0/0</span>
                </div>
                <div className="text-xs text-center py-6 opacity-50">
                  Nothing to show
                </div>
              </section>

              {/* Announcements Section */}
              <section>
                <div className="flex items-center gap-2 text-sm mb-4">
                  <Megaphone className="w-4 h-4" />
                  <span className="font-bold">Announcements</span>
                </div>
                <div className="text-xs text-center py-6 opacity-50">
                  Nothing to show
                </div>
              </section>

              {/* Notifications Section */}
              <section>
                <div className="flex items-center gap-2 text-sm mb-4">
                  <Bell className="w-4 h-4" />
                  <span className="font-bold">Notifications</span>
                </div>
                <div className="text-xs text-center py-6 opacity-50">
                  Nothing to show
                </div>
              </section>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
