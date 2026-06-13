"""
Seed Script — Built-in Themes
===============================
Run: python manage.py shell < scripts/seed_themes.py
"""

import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.themes.models import Theme

THEMES = [
    {
        "name": "Midnight",
        "slug": "midnight",
        "description": "Dark theme with deep blue accents",
        "css_variables": {
            "--bg-color": "#0f0f23",
            "--text-color": "#cccccc",
            "--sub-color": "#666688",
            "--main-color": "#e2b714",
            "--caret-color": "#e2b714",
            "--error-color": "#ca4754",
            "--error-extra-color": "#7e2a33",
            "--correct-color": "#d1d0c5",
        },
        "is_default": True,
    },
    {
        "name": "Arctic",
        "slug": "arctic",
        "description": "Clean light theme with cool tones",
        "css_variables": {
            "--bg-color": "#f0f4f8",
            "--text-color": "#2d3748",
            "--sub-color": "#a0aec0",
            "--main-color": "#3182ce",
            "--caret-color": "#3182ce",
            "--error-color": "#e53e3e",
            "--error-extra-color": "#c53030",
            "--correct-color": "#2d3748",
        },
        "is_default": True,
    },
    {
        "name": "Dracula",
        "slug": "dracula",
        "description": "Popular dark theme with vibrant colors",
        "css_variables": {
            "--bg-color": "#282a36",
            "--text-color": "#f8f8f2",
            "--sub-color": "#6272a4",
            "--main-color": "#bd93f9",
            "--caret-color": "#bd93f9",
            "--error-color": "#ff5555",
            "--error-extra-color": "#ff6e6e",
            "--correct-color": "#f8f8f2",
        },
        "is_default": True,
    },
    {
        "name": "Nord",
        "slug": "nord",
        "description": "Arctic-inspired color palette",
        "css_variables": {
            "--bg-color": "#2e3440",
            "--text-color": "#eceff4",
            "--sub-color": "#4c566a",
            "--main-color": "#88c0d0",
            "--caret-color": "#88c0d0",
            "--error-color": "#bf616a",
            "--error-extra-color": "#d08770",
            "--correct-color": "#eceff4",
        },
        "is_default": True,
    },
    {
        "name": "Monokai",
        "slug": "monokai",
        "description": "Classic code editor theme",
        "css_variables": {
            "--bg-color": "#272822",
            "--text-color": "#f8f8f2",
            "--sub-color": "#75715e",
            "--main-color": "#a6e22e",
            "--caret-color": "#f92672",
            "--error-color": "#f92672",
            "--error-extra-color": "#fd5ff0",
            "--correct-color": "#f8f8f2",
        },
        "is_default": True,
    },
    {
        "name": "Tokyo Night",
        "slug": "tokyo-night",
        "description": "Inspired by Tokyo city lights at night",
        "css_variables": {
            "--bg-color": "#1a1b26",
            "--text-color": "#c0caf5",
            "--sub-color": "#565f89",
            "--main-color": "#7aa2f7",
            "--caret-color": "#7aa2f7",
            "--error-color": "#f7768e",
            "--error-extra-color": "#db4b4b",
            "--correct-color": "#c0caf5",
        },
        "is_default": True,
    },
    {
        "name": "Gruvbox Dark",
        "slug": "gruvbox-dark",
        "description": "Retro groove color scheme",
        "css_variables": {
            "--bg-color": "#282828",
            "--text-color": "#ebdbb2",
            "--sub-color": "#928374",
            "--main-color": "#fabd2f",
            "--caret-color": "#fabd2f",
            "--error-color": "#fb4934",
            "--error-extra-color": "#cc241d",
            "--correct-color": "#ebdbb2",
        },
        "is_default": True,
    },
    {
        "name": "One Dark",
        "slug": "one-dark",
        "description": "Atom editor-inspired dark theme",
        "css_variables": {
            "--bg-color": "#282c34",
            "--text-color": "#abb2bf",
            "--sub-color": "#5c6370",
            "--main-color": "#61afef",
            "--caret-color": "#528bff",
            "--error-color": "#e06c75",
            "--error-extra-color": "#be5046",
            "--correct-color": "#abb2bf",
        },
        "is_default": True,
    },
    {
        "name": "Catppuccin Mocha",
        "slug": "catppuccin-mocha",
        "description": "Soothing pastel theme for the high-spirited",
        "css_variables": {
            "--bg-color": "#1e1e2e",
            "--text-color": "#cdd6f4",
            "--sub-color": "#6c7086",
            "--main-color": "#cba6f7",
            "--caret-color": "#f5c2e7",
            "--error-color": "#f38ba8",
            "--error-extra-color": "#eba0ac",
            "--correct-color": "#cdd6f4",
        },
        "is_default": True,
    },
    {
        "name": "Solarized Dark",
        "slug": "solarized-dark",
        "description": "Precision colors for machines and people",
        "css_variables": {
            "--bg-color": "#002b36",
            "--text-color": "#839496",
            "--sub-color": "#586e75",
            "--main-color": "#b58900",
            "--caret-color": "#b58900",
            "--error-color": "#dc322f",
            "--error-extra-color": "#cb4b16",
            "--correct-color": "#93a1a1",
        },
        "is_default": True,
    },
    {
        "name": "Cyberpunk",
        "slug": "cyberpunk",
        "description": "Neon-infused futuristic theme",
        "css_variables": {
            "--bg-color": "#0a0a0a",
            "--text-color": "#00ff41",
            "--sub-color": "#006b1d",
            "--main-color": "#ff00ff",
            "--caret-color": "#00ffff",
            "--error-color": "#ff0000",
            "--error-extra-color": "#cc0000",
            "--correct-color": "#00ff41",
        },
        "is_default": True,
    },
    {
        "name": "Rose Pine",
        "slug": "rose-pine",
        "description": "All natural pine, faux fox fur and a bit of soho vibes",
        "css_variables": {
            "--bg-color": "#191724",
            "--text-color": "#e0def4",
            "--sub-color": "#6e6a86",
            "--main-color": "#ebbcba",
            "--caret-color": "#eb6f92",
            "--error-color": "#eb6f92",
            "--error-extra-color": "#b4637a",
            "--correct-color": "#e0def4",
        },
        "is_default": True,
    },
    {
        "name": "Sunset",
        "slug": "sunset",
        "description": "Warm sunset-inspired gradient theme",
        "css_variables": {
            "--bg-color": "#1a1423",
            "--text-color": "#f0d9b5",
            "--sub-color": "#7a5c58",
            "--main-color": "#ff7b72",
            "--caret-color": "#ffa657",
            "--error-color": "#ff4444",
            "--error-extra-color": "#cc3333",
            "--correct-color": "#f0d9b5",
        },
        "is_default": True,
    },
    {
        "name": "Ocean",
        "slug": "ocean",
        "description": "Deep ocean blue theme",
        "css_variables": {
            "--bg-color": "#0d1117",
            "--text-color": "#c9d1d9",
            "--sub-color": "#484f58",
            "--main-color": "#58a6ff",
            "--caret-color": "#58a6ff",
            "--error-color": "#f85149",
            "--error-extra-color": "#da3633",
            "--correct-color": "#c9d1d9",
        },
        "is_default": True,
    },
    {
        "name": "Paper",
        "slug": "paper",
        "description": "Clean minimalist light theme",
        "css_variables": {
            "--bg-color": "#faf4ed",
            "--text-color": "#575279",
            "--sub-color": "#9893a5",
            "--main-color": "#286983",
            "--caret-color": "#286983",
            "--error-color": "#b4637a",
            "--error-extra-color": "#d7827e",
            "--correct-color": "#575279",
        },
        "is_default": True,
    },
]


def seed():
    created_count = 0
    updated_count = 0
    for theme_data in THEMES:
        theme, created = Theme.objects.update_or_create(
            slug=theme_data["slug"],
            defaults=theme_data,
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"✅ Themes: {created_count} created, {updated_count} updated")


if __name__ == "__main__":
    seed()
else:
    seed()
