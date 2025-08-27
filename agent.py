# agent.py
import os
import threading
import traceback
from playwright.sync_api import sync_playwright
from automacao1.main import run as venda_voalle
import keyboard  # pip install keyboard

# (opcional) carregar variáveis do .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ----- lock para evitar duas tarefas ao mesmo tempo -----
TASK_LOCK = threading.Lock()

def hotkey_task(fn, ctx):
    def wrapper():
        if not TASK_LOCK.acquire(blocking=False):
            print("⚠️  Já existe uma tarefa rodando. Aguarde terminar.")
            return
        try:
            fn(ctx)
            print("✅ Tarefa concluída.")
        except Exception as e:
            print(f"❌ Erro na tarefa: {e}")
            traceback.print_exc()
        finally:
            TASK_LOCK.release()
    return wrapper

def sanity_check(ctx):
    """Abre example.com só para testar rede. Fecha em seguida."""
    try:
        p = ctx.new_page()
        p.goto("https://example.com", timeout=20000, wait_until="domcontentloaded")
        print("🔌 Rede OK (consegui abrir https://example.com).")
        p.close()
        return True
    except Exception as e:
        print("❌ Falha no teste de rede (example.com):", e)
        return False

def open_startup_tabs(ctx):
    """Abre STARTUP_URLS sem deixar aba about:blank pendurada e com logs claros."""
    raw = os.getenv("STARTUP_URLS", "").strip()
    print(f"🛈 STARTUP_URLS={raw!r}")
    if not raw:
        return
    urls = [u.strip() for u in raw.split(",") if u.strip()]
    if not urls:
        print("⚠️ Nenhuma URL válida em STARTUP_URLS.")
        return

    try:
        # Reaproveita a primeira aba se for em branco
        if ctx.pages and ctx.pages[0].url in ("about:blank", "chrome://newtab/"):
            first = urls.pop(0)
            print(f"↪️  Navegando a primeira aba para: {first}")
            ctx.pages[0].goto(first, wait_until="domcontentloaded", timeout=45000)

        # Abre demais em novas abas
        for u in urls:
            print(f"➕ Abrindo nova aba: {u}")
            page = ctx.new_page()
            page.goto(u, wait_until="domcontentloaded", timeout=45000)

        # Fecha qualquer about:blank que tenha sobrado
        blanks = [p for p in ctx.pages if p.url == "about:blank"]
        for p in blanks:
            try:
                p.close()
            except Exception:
                pass

        print("✅ Abas iniciais prontas.")
    except Exception as e:
        print("❌ Erro ao abrir STARTUP_URLS:", e)

def main():
    user_data_dir = os.getenv("USER_DATA_DIR")
    if not user_data_dir:
        raise RuntimeError(
            "Defina USER_DATA_DIR no .env apontando para a PASTA do perfil do Chrome "
            '(ex.: C:\\ChromeFenix ou C:\\Users\\SEU\\AppData\\Local\\Google\\Chrome\\User Data).'
        )

    channel = os.getenv("BROWSER_CHANNEL", "chrome")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    chrome_profile = os.getenv("CHROME_PROFILE", "").strip()

    # --- monta args (igual você já tinha) ---
    args = []
    win_size = os.getenv("WINDOW_SIZE", "").strip()
    if win_size:
        args.append(f"--window-size={win_size}")
    else:
        if os.getenv("FULLSCREEN", "false").lower() == "true":
            args.append("--start-fullscreen")
        else:
            args.append("--start-maximized")

    dsf = os.getenv("CHROME_DSF", "").strip()
    if dsf:
        args.extend([f"--force-device-scale-factor={dsf}", "--high-dpi-support=1"])
    if chrome_profile:
        args.append(f"--profile-directory={chrome_profile}")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel=channel,
            headless=headless,
            args=args,
        )

        # ✅ COLOQUE AQUI:
        ok = sanity_check(ctx)
        if not ok:
            print("⚠️ Verifique sua conexão/rede/proxy. Vou manter o agente aberto mesmo assim.")

        # depois do teste, abra as abas iniciais
        open_startup_tabs(ctx)

        print("🚀 Agente ativo.")
        print(f"Perfil base: {user_data_dir}")
        if chrome_profile:
            print(f"Profile Directory: {chrome_profile}")
        if win_size:
            print(f"Window size: {win_size}")
        if dsf:
            print(f"Device scale factor: {dsf}")

        print("Atalhos:")
        print("  CTRL+F7        -> venda_voalle (automacao1)")
        print("  CTRL+SHIFT+Q   -> sair (fecha o Chrome do agente)")

        keyboard.add_hotkey("ctrl+f7", hotkey_task(venda_voalle, ctx))
        keyboard.wait("ctrl+shift+q")
        ctx.close()

if __name__ == "__main__":
    main()
