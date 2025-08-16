# test_config.py
import time
from playwright.sync_api import sync_playwright
from common.config import CDP_ENDPOINT, TIMEOUT
from common.utils import log_info, get_timestamp, ensure_dir

def test_cdp_connection():
    """Testa a conexão CDP e traz a janela do navegador para frente"""
    log_info("=== Iniciando teste de conexão CDP ===")
    
    try:
        # Conecta ao Chrome via CDP
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(CDP_ENDPOINT)
        log_info(f"Conectado ao CDP em: {CDP_ENDPOINT}")
        
        # Cria uma nova página
        page = browser.new_page()
        log_info("Nova página criada")
        
        # Define um timeout padrão
        page.set_default_timeout(TIMEOUT)
        
        # Abre uma página de teste
        test_url = "https://www.google.com"
        log_info(f"Navegando para: {test_url}")
        page.goto(test_url)
        
        # Verifica se a página carregou corretamente
        assert "Google" in page.title()
        log_info("Página carregada com sucesso!")
        
        # Traz a janela do navegador para frente
        page.bring_front()
        log_info("Janela do navegador trazida para frente")
        
        # Tira um screenshot como evidência
        screenshots_dir = ensure_dir(Path("logs/screenshots"))
        screenshot_path = screenshots_dir / f"cdp_test_{get_timestamp()}.png"
        page.screenshot(path=str(screenshot_path))
        log_info(f"Screenshot salvo em: {screenshot_path}")
        
        # Aguarda 5 segundos para visualização manual
        log_info("Aguardando 5 segundos para visualização manual...")
        time.sleep(5)
        
        # Fecha a página (mas mantém o navegador aberto)
        page.close()
        log_info("Página fechada (navegador permanece aberto)")
        
        print("\n✅ Teste CDP concluído com sucesso!")
        print("📸 Screenshot salvo em:", screenshot_path)
        print("🌐 Janela do navegador foi trazida para frente")
        
        return True
        
    except Exception as e:
        log_error(f"Erro no teste CDP: {str(e)}")
        print(f"\n❌ Falha no teste: {str(e)}")
        return False

if __name__ == "__main__":
    # Executa o teste
    success = test_cdp_connection()
    
    # Exibe mensagem final
    if success:
        print("\n🎉 Tudo funcionando! A conexão CDP está operacional.")
    else:
        print("\n⚠️ Verifique:")
        print("1. Se o Chrome CDP está aberto (atalho 'Chrome – Work CDP')")
        print("2. Se a porta 9222 está acessível (tente abrir http://localhost:9222)")
        print("3. Se o arquivo .env contém CDP_ENDPOINT=http://localhost:9222")