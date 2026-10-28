import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
MODEL = os.getenv('OLLAMA_MODEL', 'qwen3:4b-instruct')
# Solo servicio local: no usa API de pago ni proveedor cloud.
OLLAMA_URL = 'http://127.0.0.1:11434'
SKILL_PATH = ROOT / '02_backend_y_mcp/skills/auditar_ventas/SKILL.md'
