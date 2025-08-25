# agent.py
import os
import threading
import traceback
from playwright.sync_api import sync_playwright
import keyboard  # pip install keyboard

# ----- lock para evitar duas tarefas ao mesmo tempo -----
TASK_LOCK = threading.Lock()

def hotkey_task(fn, ctx):
    """Envolve a função da tarefa para impedir reentrância e logar erros."""
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

# ----- SUAS TAREFAS (exemplo mínimo) -----
def tarefa_voalle(ctx):
    # OBS: se você quer reutilizar SEMPRE a aba do Voalle,
    # troque esse trecho para usar o helper get_or_open() depois.
    page = ctx.new_page()
    page.goto(os.getenv("BASE_URL", "https://exemplo.com"))
    # ... automação aqui ...
    # Se quiser manter a aba aberta, REMOVA a linha abaixo:
    # page.close()

def main():
    user_data_dir = os.getenv("USER_DATA_DIR")
    channel = os.getenv("BROWSER_CHANNEL", "chrome")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel=channel,
            headless=False,
            args=["--start-maximized"]
        )

        print("🚀 Agente ativo.")
        print("Atalhos:")
        print("  CTRL+F7        -> tarefa_voalle")
        print("  CTRL+SHIFT+Q   -> sair (fecha o Chrome do agente)")

        # registre as hotkeys usando o wrapper com lock
        keyboard.add_hotkey("ctrl+f7", hotkey_task(tarefa_voalle, ctx))

        # Exemplo: mais automações
        # from automacao2.main import run as outra_tarefa
        # keyboard.add_hotkey("ctrl+f8", hotkey_task(outra_tarefa, ctx))

        # mantém o processo vivo até você mandar sair
        keyboard.wait("ctrl+shift+q")

        # encerra limpo
        ctx.close()

if __name__ == "__main__":
    main()
