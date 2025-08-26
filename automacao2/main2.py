# automacao2/main.py
from common.tabs import get_or_open

def run(ctx):
    page = get_or_open(ctx, match_or_url="seu-sistema", ensure_url="https://url-do-sistema")
    # ... passos desta automação ...
