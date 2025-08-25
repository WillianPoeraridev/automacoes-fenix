# common/tabs.py
from typing import Optional
from playwright.sync_api import BrowserContext, Page, TimeoutError

def _match(p: Page, needle: str) -> bool:
    needle = needle.lower()
    try:
        if needle in (p.url or "").lower():
            return True
        t = p.title() or ""
        return needle in t.lower()
    except Exception:
        return False

def find_page(ctx: BrowserContext, match: str) -> Optional[Page]:
    # pega a MAIS RECENTE que bate (última da lista)
    matches = [p for p in ctx.pages if _match(p, match)]
    return matches[-1] if matches else None

def get_or_open(
    ctx: BrowserContext,
    match_or_url: str,
    ensure_url: str | None = None,
    wait_selector: str | None = None,
    foreground: bool = True,
    wait_until: str = "domcontentloaded",
) -> Page:
    """
    - match_or_url: fragmento para achar a aba (ex.: "voalle") ou uma URL.
    - ensure_url: se a aba encontrada não estiver nela, navega para cá.
    - wait_selector: opcional, espera esse seletor aparecer.
    """
    page = find_page(ctx, match_or_url) or find_page(ctx, ensure_url or "")
    if not page:
        page = ctx.new_page()
        target = ensure_url or match_or_url
        page.goto(target, wait_until=wait_until)

    elif ensure_url and ensure_url.lower() not in (page.url or "").lower():
        page.goto(ensure_url, wait_until=wait_until)

    if foreground:
        try:
            page.bring_to_front()
        except Exception:
            pass

    if wait_selector:
        try:
            page.wait_for_selector(wait_selector, timeout=15000)
        except TimeoutError:
            # segue o baile mesmo que o seletor demore/nao exista
            pass

    return page
