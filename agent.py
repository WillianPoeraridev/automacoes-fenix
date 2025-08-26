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
    """Impede reentrância e loga erros da tarefa."""
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

def open_startup_tabs(ctx):
    """Abre as abas iniciais definidas em STARTUP_URLS (se houver)."""
    raw = os.getenv("STARTUP_URLS", "").strip()
    if not raw:
        return
    urls = [u.strip() for u in raw.split(",") if u.strip()]
    opened = []
    for u in urls:
        try:
            page = ctx.new_page()
            page.goto(u, wait_until="domcontentloaded")
            opened.append(u)
        except Exception as e:
            print(f"⚠️ Não consegui abrir {u}: {e}")
    if opened and ctx.pages:
        try:
            ctx.pages[-1].bring_to_front()
        except Exception:
            pass
        print("🟢 Abas iniciais abertas:", ", ".join(opened))

def main():
    user_data_dir = os.getenv("USER_DATA_DIR")
    if not user_data_dir:
        raise RuntimeError(
            "Defina USER_DATA_DIR no .env apontando para a PASTA do perfil do Chrome "
            '(ex.: C:\\Users\\SEU\\AppData\\Local\\Google\\Chrome\\User Data ou C:\\ChromeFenix).'
        )

    channel = os.getenv("BROWSER_CHANNEL", "chrome")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    chrome_profile = os.getenv("CHROME_PROFILE")  # ex.: Default

    # -------- ARGS do Chrome (janela e escala/DPI) --------
    args = []
    win_size = os.getenv("WINDOW_SIZE", "").strip()  # ex.: 1366,768
    if win_size:
        args.append(f"--window-size={win_size}")
    else:
        args.append("--start-maximized")

    dsf = os.getenv("CHROME_DSF", "").strip()  # ex.: 1  (100%); 0.9 (~90%)
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

        print("🚀 Agente ativo.")
        print(f"Perfil base: {user_data_dir}")
        if chrome_profile:
            print(f"Profile Directory: {chrome_profile}")
        if win_size:
            print(f"Window size: {win_size}")
        if dsf:
            print(f"Device scale factor: {dsf}")

        open_startup_tabs(ctx)

        print("Atalhos:")
        print("  CTRL+F7        -> venda_voalle (automacao1)")
        print("  CTRL+SHIFT+Q   -> sair (fecha o Chrome do agente)")

        keyboard.add_hotkey("ctrl+f7", hotkey_task(venda_voalle, ctx))

        keyboard.wait("ctrl+shift+q")
        ctx.close()

if __name__ == "__main__":
    main()
