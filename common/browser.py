# common/browser.py
from playwright.sync_api import sync_playwright
from .config import HEADLESS
from .utils import log_info

class Browser:
    """
    Context manager para abrir navegador Playwright em 1 linha:
    with Browser() as page:
        page.goto("https://exemplo.com")
    """
    def __enter__(self):
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch(headless=HEADLESS)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        log_info("Browser iniciado")
        return self.page

    def __exit__(self, exc_type, exc, tb):
        self.context.close()
        self.browser.close()
        self._pw.stop()
        log_info("Browser fechado")

def get_browser(cdp_endpoint):
    """
    Conecta a uma instância do Chrome já aberta via CDP.
    Retorna o objeto browser.
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.connect_over_cdp(cdp_endpoint)
    return browser