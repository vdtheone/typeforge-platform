import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api, useAuthStore } from '@/utils/api';
import { X, Loader2 } from 'lucide-react';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const response = await api.post('/auth/login/', { username, password });
        // Depending on dj-rest-auth config, it usually returns { access: string, user: User } or { key: string }
        const token = response.data.access || response.data.key || response.data.access_token;
        const user = response.data.user;
        setAuth(user, token);
        onClose();
      } else {
        const response = await api.post('/auth/register/', { 
          username, 
          email, 
          password1: password, 
          password2: password 
        });
        const token = response.data.access || response.data.key || response.data.access_token;
        const user = response.data.user;
        setAuth(user, token);
        onClose();
      }
    } catch (err: any) {
      setError(
        err.response?.data?.non_field_errors?.[0] || 
        err.response?.data?.detail || 
        'An error occurred. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 z-50 backdrop-blur-sm"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-[var(--bg-color)] border border-[var(--sub-color)]/20 rounded-xl shadow-2xl z-50 p-6 flex flex-col font-mono"
          >
            <div className="flex justify-between items-center mb-6 text-[var(--text-color)]">
              <h2 className="text-xl font-bold">{isLogin ? 'login' : 'register'}</h2>
              <button onClick={onClose} className="hover:text-[var(--main-color)] transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            {error && (
              <div className="bg-[var(--error-color)]/10 text-[var(--error-color)] p-3 rounded-lg mb-4 text-sm border border-[var(--error-color)]/20">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs text-[var(--sub-color)]">username</label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="bg-[var(--sub-color)]/10 border border-[var(--sub-color)]/20 rounded-lg p-2.5 text-[var(--text-color)] focus:outline-none focus:border-[var(--main-color)] transition-colors"
                />
              </div>

              {!isLogin && (
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-[var(--sub-color)]">email</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-[var(--sub-color)]/10 border border-[var(--sub-color)]/20 rounded-lg p-2.5 text-[var(--text-color)] focus:outline-none focus:border-[var(--main-color)] transition-colors"
                  />
                </div>
              )}

              <div className="flex flex-col gap-1.5">
                <label className="text-xs text-[var(--sub-color)]">password</label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-[var(--sub-color)]/10 border border-[var(--sub-color)]/20 rounded-lg p-2.5 text-[var(--text-color)] focus:outline-none focus:border-[var(--main-color)] transition-colors"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="mt-2 bg-[var(--main-color)] text-[var(--bg-color)] font-bold py-2.5 rounded-lg hover:opacity-90 transition-opacity flex justify-center items-center h-[44px]"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (isLogin ? 'sign in' : 'sign up')}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-[var(--sub-color)]">
              {isLogin ? "don't have an account? " : "already have an account? "}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-[var(--main-color)] hover:underline"
              >
                {isLogin ? 'register' : 'login'}
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
