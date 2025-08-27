# automacao1/main.py
from common.tabs import get_or_open

VOALLE_URL   = "https://erp.fenixwireless.com.br/assignments"
VOALLE_MATCH = "fenixwireless.com.br"

def run(ctx):
    page = get_or_open(
        ctx,
        match_or_url=VOALLE_MATCH,   # reutiliza a aba se já existir
        ensure_url=VOALLE_URL,       # ou abre /assignments
        wait_selector="body"
    )
    print("✅ Voalle focado/aberto (sem alterar layout).")
