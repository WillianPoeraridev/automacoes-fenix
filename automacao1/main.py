# automacao1/main.py
from common.tabs import get_or_open
from playwright.sync_api import Page

VOALLE_URL   = "https://erp.fenixwireless.com.br/assignments"
VOALLE_MATCH = "fenixwireless.com.br"   # fragmento de URL/título para achar a aba existente

# --- CSS para remover max-width e deixar o layout fluido ---
CSS_WIDE = """
html, body { max-width: none !important; width: 100% !important; }
#app, .app, .container, .content, .wrapper, .page, .layout, .root, .main, .container-fluid {
  max-width: none !important;
  width: 100% !important;
}
aside, .sidebar, [class*="sidebar"] {
  max-width: 240px !important; width: 240px !important;
}
body { overflow-x: hidden !important; }
"""

def widen_layout(page: Page) -> None:
    try:
        page.add_style_tag(content=CSS_WIDE)
    except Exception:
        pass

def run(ctx):
    # Reutiliza a aba do Voalle (ou abre se não existir) e espera a página carregar
    page = get_or_open(
        ctx,
        match_or_url=VOALLE_MATCH,   # se a aba já existir, reutiliza
        ensure_url=VOALLE_URL,       # se não existir, navega para /assignments
        wait_selector="body"
    )

    # Deixa o layout ocupar toda a largura
    widen_layout(page)

    # (opcional) marca visualmente a página para confirmar que a automação tocou nela
    # page.evaluate("""
    #     document.body.style.outline='3px solid lime';
    #     document.title = '🟢 [AUTOMAÇÃO] ' + document.title;
    # """)

    print("✅ Voalle (/assignments) focado/aberto na MESMA aba e com layout alargado.")