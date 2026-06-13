'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, useAuthStore } from '@/utils/api';
import { UserPlus, LogIn, Code, Mail, User, Key, Check, Hash, MessageSquare } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  // Login State
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // Register State
  const [regUsername, setRegUsername] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regPassword2, setRegPassword2] = useState('');
  const [regError, setRegError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');
    setIsLoggingIn(true);
    try {
      const response = await api.post('/auth/login/', { username: loginEmail, password: loginPassword });
      const token = response.data.access || response.data.key || response.data.access_token;
      setAuth(response.data.user, token);
      router.push('/');
    } catch (err: any) {
      setLoginError(err.response?.data?.non_field_errors?.[0] || err.response?.data?.detail || 'Login failed.');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError('');
    
    if (regPassword !== regPassword2) {
      setRegError('Passwords do not match');
      return;
    }

    setIsRegistering(true);
    try {
      const response = await api.post('/auth/register/', { 
        username: regUsername, 
        email: regEmail, 
        password1: regPassword, 
        password2: regPassword2 
      });
      const token = response.data.access || response.data.key || response.data.access_token;
      setAuth(response.data.user, token);
      router.push('/');
    } catch (err: any) {
      setRegError(err.response?.data?.non_field_errors?.[0] || 'Registration failed.');
    } finally {
      setIsRegistering(false);
    }
  };

  const handleSocialLogin = (provider: string) => {
    // In a real application, this would redirect to the OAuth provider
    // window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/${provider}/login/`;
    alert(`${provider} login is not fully configured in this environment (requires OAuth Client IDs).`);
  };

  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col md:flex-row gap-16 md:gap-32 mt-12 md:mt-24 px-4">
      {/* Register Section */}
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex-1 flex flex-col font-mono"
      >
        <div className="flex items-center gap-2 text-[var(--sub-color)] mb-6 text-sm">
          <UserPlus className="w-4 h-4" />
          <span>register</span>
        </div>
        
        {regError && <div className="text-[var(--error-color)] mb-4 text-xs">{regError}</div>}
        
        <form onSubmit={handleRegister} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="username"
            value={regUsername}
            onChange={(e) => setRegUsername(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          <input
            type="email"
            placeholder="email"
            value={regEmail}
            onChange={(e) => setRegEmail(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          <input
            type="password"
            placeholder="password"
            value={regPassword}
            onChange={(e) => setRegPassword(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          <input
            type="password"
            placeholder="verify password"
            value={regPassword2}
            onChange={(e) => setRegPassword2(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          
          <button 
            type="submit" 
            disabled={isRegistering}
            className="mt-4 flex items-center justify-center gap-2 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/10 py-3 rounded-lg transition-colors"
          >
            <UserPlus className="w-4 h-4" /> {isRegistering ? 'signing up...' : 'sign up'}
          </button>
        </form>
      </motion.div>

      {/* Login Section */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex-1 flex flex-col font-mono"
      >
        <div className="flex items-center gap-2 text-[var(--sub-color)] mb-6 text-sm">
          <LogIn className="w-4 h-4" />
          <span>login</span>
        </div>

        {loginError && <div className="text-[var(--error-color)] mb-4 text-xs">{loginError}</div>}

        {/* OAuth Buttons */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <button 
            type="button"
            onClick={() => handleSocialLogin('Google')}
            className="flex-1 bg-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] py-3 rounded-lg transition-colors flex justify-center items-center"
            title="Login with Google"
          >
             <span className="font-bold">G</span>
          </button>
          <button 
            type="button"
            onClick={() => handleSocialLogin('GitHub')}
            className="flex-1 bg-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] py-3 rounded-lg transition-colors flex justify-center items-center"
            title="Login with GitHub"
          >
             <Code className="w-5 h-5" />
          </button>
          <button 
            type="button"
            onClick={() => handleSocialLogin('Twitter')}
            className="flex-1 bg-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] py-3 rounded-lg transition-colors flex justify-center items-center"
            title="Login with Twitter"
          >
             <Hash className="w-5 h-5" />
          </button>
          <button 
            type="button"
            onClick={() => handleSocialLogin('Discord')}
            className="flex-1 bg-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/20 text-[var(--sub-color)] hover:text-[var(--text-color)] py-3 rounded-lg transition-colors flex justify-center items-center"
            title="Login with Discord"
          >
             <MessageSquare className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex items-center gap-4 text-[var(--sub-color)] mb-6 text-sm">
          <div className="flex-1 h-px bg-[var(--sub-color)]/20"></div>
          <span>or</span>
          <div className="flex-1 h-px bg-[var(--sub-color)]/20"></div>
        </div>

        <form onSubmit={handleLogin} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="email or username"
            value={loginEmail}
            onChange={(e) => setLoginEmail(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          <input
            type="password"
            placeholder="password"
            value={loginPassword}
            onChange={(e) => setLoginPassword(e.target.value)}
            className="w-full bg-[var(--sub-color)]/10 text-[var(--text-color)] placeholder:text-[var(--sub-color)] px-4 py-3 rounded-lg focus:outline-none focus:bg-[var(--sub-color)]/20 transition-colors"
            required
          />
          
          <div className="flex items-center gap-2 mt-2 text-sm text-[var(--sub-color)] cursor-pointer hover:text-[var(--text-color)] transition-colors w-fit">
            <div className="text-[var(--main-color)]"><Check className="w-4 h-4" /></div>
            remember me
          </div>

          <button 
            type="submit" 
            disabled={isLoggingIn}
            className="mt-4 flex items-center justify-center gap-2 text-[var(--sub-color)] hover:text-[var(--text-color)] hover:bg-[var(--sub-color)]/10 py-3 rounded-lg transition-colors"
          >
            <LogIn className="w-4 h-4" /> {isLoggingIn ? 'signing in...' : 'sign in'}
          </button>

          <div className="mt-4 text-center text-xs text-[var(--sub-color)] hover:text-[var(--text-color)] cursor-pointer transition-colors">
            forgot password?
          </div>
        </form>
      </motion.div>
    </div>
  );
}
