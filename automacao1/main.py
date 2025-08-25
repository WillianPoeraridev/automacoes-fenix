"""
Novo fluxo:
1. Focar/abrir https://erp.fenixwireless.com.br/
2. Clicar no ícone/menu “PESQUISA CLIENTES”.
3. Esperar a tela /SearchPeople carregar, digitar CPF 02690676044 e buscar.
4. Focar/abrir PipeRun, clicar no 1º cliente da fila.
"""

from common.browser import Browser
from common.utils import log_info
from playwright.sync_api import TimeoutError

# ---------------- URLs ----------------
VOALLE_HOME  = "https://erp.fenixwireless.com.br/"
VOALLE_SEARCH = "https://erp.fenixwireless.com.br/SearchPeople"
PIPERUN_URL = "https://rapidanet.cxm.pipe.run/agent"
CPF = "02690676044"

# ------------- seletores ---------------
BTN_PESQ = 'a[title="PESQUISA CLIENTES"]'
INPUT_BUSCA = 'input#search, input[name="search"]'   # tente id OU name
CLIENTE_PRIMEIRO = "div.talk-button"
# ---------------------------------------

def open_or_focus(ctx, prefix: str, full: str):
    """Retorna aba já existente que começa com `prefix` ou abre nova."""
    p = next((p for p in ctx.pages if p.url.startswith(prefix)), None)
    if not p:
        p = ctx.new_page()
        p.goto(full, wait_until="domcontentloaded")
        log_info(f"Nova aba em {full}")
    else:
        log_info(f"Aba já existente → {p.url}")
    p.bring_to_front()          # garante janela na frente
    return p

def run():
    with Browser() as dummy:
        ctx = dummy.context

        # ---------- 1. Home do Voalle ----------
        voalle = open_or_focus(ctx, VOALLE_HOME, VOALLE_HOME)

        # clica no menu “Pesquisa Clientes”
        if voalle.locator(BTN_PESQ).count():
            voalle.click(BTN_PESQ)
            log_info("Cliquei em PESQUISA CLIENTES")
        else:
            print("‼️  Não achei o botão PESQUISA CLIENTES; ajuste BTN_PESQ se necessário.")
            return

        # ---------- 2. Tela /SearchPeople ----------
        try:
            voalle.wait_for_url("**/SearchPeople*", timeout=10000)
            voalle.wait_for_selector(INPUT_BUSCA, timeout=10000)
        except TimeoutError:
            print("‼️  Campo de busca não apareceu.\n"
                  "     Copie o seletor exato no DevTools e ajuste INPUT_BUSCA.")
            return

        voalle.fill(INPUT_BUSCA, CPF)
        voalle.keyboard.press("Enter")
        log_info(f"Enviado CPF {CPF} no Voalle")

        # ---------- 3. PipeRun ----------
        pipe = open_or_focus(ctx, PIPERUN_URL, PIPERUN_URL)

        try:
            pipe.wait_for_selector(CLIENTE_PRIMEIRO, timeout=10000)
            pipe.click(CLIENTE_PRIMEIRO)
            log_info("Clicado primeiro cliente na fila PipeRun")
        except TimeoutError:
            print("‼️  Cliente não encontrado; ajuste CLIENTE_PRIMEIRO se mudou o HTML.")

        input("✅  Fluxo terminado. Enter para desconectar…")

if __name__ == "__main__":
    run()
