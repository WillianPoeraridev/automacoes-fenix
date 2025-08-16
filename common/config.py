"""
Configurações globais carregadas do .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv  # type: ignore

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent

# Carrega o arquivo .env (uma única vez na execução)
ENV_FILE = ROOT_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    print(f"AVISO: Arquivo .env não encontrado em {ENV_FILE}")

# Variáveis de configuração com valores padrão
BASE_URL: str = os.getenv("BASE_URL", "https://example.com")
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
USER_EMAIL: str | None = os.getenv("USER_EMAIL")
USER_PASSWORD: str | None = os.getenv("USER_PASSWORD")

# Configurações específicas para o projeto
CDP_ENDPOINT: str = os.getenv("CDP_ENDPOINT", "http://localhost:9222")
TIMEOUT: int = int(os.getenv("TIMEOUT", "10000"))  # 10 segundos padrão