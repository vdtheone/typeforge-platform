import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ThemeVariables {
  '--bg-color': string;
  '--text-color': string;
  '--sub-color': string;
  '--main-color': string;
  '--caret-color': string;
  '--error-color': string;
  '--error-extra-color': string;
  '--correct-color': string;
}

export interface Theme {
  name: string;
  slug: string;
  css_variables: ThemeVariables;
}

// Default Theme (Midnight)
export const defaultTheme: Theme = {
  name: 'Midnight',
  slug: 'midnight',
  css_variables: {
    '--bg-color': '#0f0f23',
    '--text-color': '#cccccc',
    '--sub-color': '#666688',
    '--main-color': '#e2b714',
    '--caret-color': '#e2b714',
    '--error-color': '#ca4754',
    '--error-extra-color': '#7e2a33',
    '--correct-color': '#d1d0c5',
  },
};

interface ThemeState {
  currentTheme: Theme;
  setTheme: (theme: Theme) => void;
  applyTheme: (theme: Theme) => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      currentTheme: defaultTheme,
      
      setTheme: (theme: Theme) => {
        set({ currentTheme: theme });
        get().applyTheme(theme);
      },
      
      applyTheme: (theme: Theme) => {
        if (typeof window !== 'undefined') {
          const root = document.documentElement;
          Object.entries(theme.css_variables).forEach(([key, value]) => {
            root.style.setProperty(key, value);
          });
        }
      },
    }),
    {
      name: 'typeforge-theme-storage',
      onRehydrateStorage: () => (state) => {
        // Re-apply theme to DOM when Zustand restores state from localStorage
        if (state) {
          state.applyTheme(state.currentTheme);
        }
      },
    }
  )
);
