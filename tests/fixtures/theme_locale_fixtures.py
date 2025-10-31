"""Theme and localization fixtures.

Works with apps that persist theme/locale in localStorage or on <html data-theme/lang>.
"""
from __future__ import annotations

def set_theme(page, theme: str):
    """Set theme to 'light' or 'dark' (extend if app supports more)."""
    page.add_init_script("""
        (theme) => {
          try { document.documentElement.setAttribute('data-theme', theme); localStorage.setItem('theme', theme);} catch (e) {}
        }
    """, theme)

def set_locale(page, locale: str):
    """Set locale (e.g., 'en', 'et')."""
    page.add_init_script("""
        (loc) => {
          try { document.documentElement.setAttribute('lang', loc); localStorage.setItem('locale', loc);} catch (e) {}
        }
    """, locale)
