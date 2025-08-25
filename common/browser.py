from playwright.sync_api import sync_playwright
import os

def run(task):
    with sync_playwright() as p:
        headless = os.getenv("HEADLESS", "true").lower() == "true"
        keep_open = os.getenv("KEEP_BROWSER_OPEN", "false").lower() == "true"
        user_data_dir = os.getenv("USER_DATA_DIR")
        channel = os.getenv("BROWSER_CHANNEL", "chrome")

        if user_data_dir:
            # Abre o Chrome REAL com seu perfil (persistente)
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel=channel,         # usa o Chrome instalado
                headless=headless,
                args=["--start-maximized"]
            )
            browser = context.browser
        else:
            # fallback (não recomendado p/ seu caso)
            browser = p.chromium.launch(channel=channel, headless=headless)
            context = browser.new_context()

        try:
            task(context)
        finally:
            if not keep_open:
                context.close()
