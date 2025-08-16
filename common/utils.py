"""
Utilidades genéricas (logger, helpers de tempo, etc.)
"""
import logging
from pathlib import Path
from datetime import datetime

# Diretório de logs (criado se não existir)
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Configuração do logger
logging.basicConfig(
    filename=LOGS_DIR / "automacoes.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(msg: str) -> None:
    """Abstração mínima só pra reduzir digitação nos scripts."""
    logging.info(msg)

def log_error(msg: str) -> None:
    """Registra mensagens de erro."""
    logging.error(msg)

def get_timestamp() -> str:
    """Retorna timestamp atual formatado para nomes de arquivos."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(path: Path) -> Path:
    """Garante que um diretório exista, criando se necessário."""
    path.mkdir(parents=True, exist_ok=True)
    return path