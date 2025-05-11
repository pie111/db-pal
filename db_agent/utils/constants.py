from pathlib import Path
CONFIG_DIR = Path.home() / ".db_chatcli"
CONFIG_FILE = CONFIG_DIR / "config.json"
AVAILABLE_MODEL_PROVIDERS = ['openai','google','groq','ollama']