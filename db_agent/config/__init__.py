import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
from ..utils.constants import CONFIG_DIR, CONFIG_FILE

def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_config(data):
    ensure_config_dir()
    # Load existing config if it exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
    else:
        config = {}

    # Update the configuration with new data
    config.update(data)

    # Save the updated configuration
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)

def save_api_key(api_key):
    save_config({"api_key": api_key})


def save_model_config(provider_name,model):
    save_config({"provider_name": provider_name,"model": model})


def save_db_info(host, user, password, database, port=5432):
    db_info = {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
        "port": port
    }
    save_config({"db_info": db_info})

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            return config
    return {}

def get_api_key():
    config = load_config()
    return config.get("api_key")

def get_db_info():
    config = load_config()
    return config.get("db_info")

def get_model_info():
    config = load_config()
    return [config.get("provider_name"), config.get("model") ]


