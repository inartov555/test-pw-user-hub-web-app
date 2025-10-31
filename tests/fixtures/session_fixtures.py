"""Session duration controls.

If the app reads a session ttl from localStorage, expose it; otherwise, back-end config can be modified
in fixtures via management command.
"""
from __future__ import annotations

def set_session_duration(page, minutes: int):
    page.add_init_script("""
        (mins) => {
          try { localStorage.setItem('session.ttl.minutes', String(mins)); } catch (e) {}
        }
    """, minutes)
