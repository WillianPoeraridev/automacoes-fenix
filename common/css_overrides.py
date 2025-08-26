# common/css_overrides.py
from playwright.sync_api import Page

CSS_WIDE = """
/* tornar layout fluido (genérico) */
html, body { max-width: none !important; width: 100% !important; }
#app, .app, .container, .content, .wrapper, .page, .layout, .root, .main {
  max-width: none !important;
  width: 100% !important;
}
/* se houver sidebars largas, dá uma enxugada */
aside, .sidebar, [class*="sidebar"] { max-width: 240px !important; width: 240px !important; }
/* evitar barras horizontais */
body { overflow-x: hidden !important; }
"""

# se quiser regras específicas por domínio, adicione aqui:
PER_DOMAIN = {
    "pipe.run": CSS_WIDE,
    "fenixwireless.com.br": CSS_WIDE,
}

def widen_layout(page: Page):
    try:
        host = page.url.split("/")[2] if "://" in page.url else ""
    except Exception:
        host = ""
    css = None
    for key, rules in PER_DOMAIN.items():
        if key in host:
            css = rules
            break
    if not css:
        return
    try:
        page.add_style_tag(content=css)
    except Exception:
        pass
