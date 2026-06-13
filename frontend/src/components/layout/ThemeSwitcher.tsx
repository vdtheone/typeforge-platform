'use client';

import { Paintbrush } from 'lucide-react';
import { useThemeStore } from '@/stores/theme.store';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

// Pre-packaged premium themes for the frontend demo
const THEMES = [
  {
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
  },
  {
    name: 'Dracula',
    slug: 'dracula',
    css_variables: {
      '--bg-color': '#282a36',
      '--text-color': '#f8f8f2',
      '--sub-color': '#6272a4',
      '--main-color': '#bd93f9',
      '--caret-color': '#bd93f9',
      '--error-color': '#ff5555',
      '--error-extra-color': '#ff6e6e',
      '--correct-color': '#f8f8f2',
    },
  },
  {
    name: 'Tokyo Night',
    slug: 'tokyo-night',
    css_variables: {
      '--bg-color': '#1a1b26',
      '--text-color': '#c0caf5',
      '--sub-color': '#565f89',
      '--main-color': '#7aa2f7',
      '--caret-color': '#7aa2f7',
      '--error-color': '#f7768e',
      '--error-extra-color': '#db4b4b',
      '--correct-color': '#c0caf5',
    },
  },
  {
    name: 'Paper',
    slug: 'paper',
    css_variables: {
      '--bg-color': '#faf4ed',
      '--text-color': '#575279',
      '--sub-color': '#9893a5',
      '--main-color': '#286983',
      '--caret-color': '#286983',
      '--error-color': '#b4637a',
      '--error-extra-color': '#d7827e',
      '--correct-color': '#575279',
    },
  }
];

export function ThemeSwitcher() {
  const { currentTheme, setTheme } = useThemeStore();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-[var(--sub-color)]/20 transition-colors text-[var(--sub-color)] hover:text-[var(--main-color)]"
      >
        <Paintbrush className="w-4 h-4" />
        <span className="text-sm font-medium">{currentTheme.name}</span>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="bg-[var(--bg-color)] border-[var(--sub-color)]/30 min-w-[200px] p-2">
        <div className="mb-2 px-2 py-1.5 text-xs font-semibold text-[var(--sub-color)] uppercase tracking-wider">
          Themes
        </div>
        {THEMES.map((theme) => (
          <DropdownMenuItem
            key={theme.slug}
            onClick={() => setTheme(theme as any)}
            className={`
              flex items-center gap-3 cursor-pointer rounded-md p-2 mb-1
              hover:bg-[var(--sub-color)]/20 focus:bg-[var(--sub-color)]/20 focus:text-[var(--text-color)]
              ${currentTheme.slug === theme.slug ? 'bg-[var(--main-color)]/10 text-[var(--main-color)]' : 'text-[var(--text-color)]'}
            `}
          >
            {/* Theme Color Preview */}
            <div className="flex gap-1 h-3 rounded-full overflow-hidden w-12 border border-black/10">
              <div className="w-1/3 h-full" style={{ backgroundColor: theme.css_variables['--bg-color'] }} />
              <div className="w-1/3 h-full" style={{ backgroundColor: theme.css_variables['--sub-color'] }} />
              <div className="w-1/3 h-full" style={{ backgroundColor: theme.css_variables['--main-color'] }} />
            </div>
            <span className="font-medium text-sm">{theme.name}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
