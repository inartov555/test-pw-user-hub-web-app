from __future__ import annotations
from playwright.sync_api import Page

INIT_SCRIPT = """
(() => {
  const _now = Date.now;
  let offsetMs = 0;
  Date.now = () => _now() + offsetMs;
  window.__advanceTime = (minutes) => { offsetMs += minutes * 60 * 1000; };
})();
"""

def install_time_travel(page: Page) -> None:
    """Inject a Date.now shim and helper onto the page."""
    page.add_init_script(INIT_SCRIPT)

def advance_minutes(page: Page, minutes: int) -> None:
    """Advance the logical clock by N minutes.

    Requires `install_time_travel` to have been called earlier in the test/fixture.
    """
    page.evaluate("minutes => window.__advanceTime(minutes)", minutes)
