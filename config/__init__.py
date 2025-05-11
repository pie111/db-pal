import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
from utils.constants import CONFIG_DIR, CONFIG_FILE

def get_encryption_key():
    """Get or create encryption key"""
    key_file = CONFIG_DIR / ".key"
    if not key_file.exists():
        key = Fernet.generate_key()
        key_file.write_bytes(key)
        os.chmod(key_file, 0o600)
    return key_file.read_bytes()

def encrypt_data(data):
    """Encrypt sensitive data"""
    f = Fernet(get_encryption_key())
    return f.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypt sensitive data"""
    f = Fernet(get_encryption_key())
    return json.loads(f.decrypt(encrypted_data.encode()).decode())

def ensure_config_dir():
    """Ensure config directory exists with proper permissions"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o700)

def save_config(data):
    """Save configuration with encryption for sensitive data"""
    ensure_config_dir()
    
    # Load existing config if it exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
    else:
        config = {}

    # Update the configuration with new data
    config.update(data)

    # Encrypt sensitive data
    if "api_key" in config:
        config["api_key"] = encrypt_data({"api_key": config["api_key"]})
    if "db_info" in config:
        config["db_info"] = encrypt_data(config["db_info"])

    # Save the updated configuration
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)
    
    # Set restrictive permissions
    os.chmod(CONFIG_FILE, 0o600)

def save_api_key(api_key):
    """Save API key with validation"""
    if not api_key or len(api_key) < 10:  # Basic validation
        raise ValueError("Invalid API key format")
    save_config({"api_key": api_key})

def save_model_config(provider_name,model):
    save_config({"provider_name": provider_name,"model": model})

def save_db_info(host, user, password, database, port=5432):
    """Save database information with validation"""
    if not all([host, user, password, database]):
        raise ValueError("All database fields are required")
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("Invalid port number")
    
    db_info = {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
        "port": port
    }
    save_config({"db_info": db_info})

def load_config():
    """Load and decrypt configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            
            # Decrypt sensitive data
            if "api_key" in config:
                config["api_key"] = decrypt_data(config["api_key"])["api_key"]
            if "db_info" in config:
                config["db_info"] = decrypt_data(config["db_info"])
            
            return config
    return {}

def get_api_key():
    """Get decrypted API key"""
    config = load_config()
    return config.get("api_key")

def get_db_info():
    """Get decrypted database information"""
    config = load_config()
    return config.get("db_info")

def get_model_info():
    """Get model configuration"""
    config = load_config()
    return [config.get("provider_name"), config.get("model")]

