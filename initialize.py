import os
import sys
import json
from pyngrok import ngrok

CONFIG_FILE = "config.json"

def save_config(config):
    """Enregistre la configuration dans un fichier JSON."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    print(f"Configuration saved to {CONFIG_FILE}")

def load_config():
    """Charge la configuration depuis le fichier JSON si elle existe."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        print(f"Configuration loaded from {CONFIG_FILE}")
        return config
    return None

def initialize_ngrok():
    config = load_config()
    
    # Vérification de l'auth token Ngrok
    if config is None or 'ngrok_auth_token' not in config or config['ngrok_auth_token'] is None:
        config = {}
        config['ngrok_auth_token'] = input("Enter your Ngrok auth token: ")
        save_config(config)

    try:
        ngrok.set_auth_token(config['ngrok_auth_token'])
        
        # Déconnecte tous les tunnels existants
        ngrok.disconnect("http://localhost:5000")  # Déconnecte spécifiquement le tunnel du port 5000
        ngrok.disconnect("http://0.tcp.ngrok.io")  # Déconnecte tous les autres tunnels, si nécessaire
        
        # Ouvrir un tunnel Ngrok sur le port 5000 (port Flask)
        public_url = ngrok.connect(5000)

        print(f"Ngrok tunnel opened at: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error initializing Ngrok: {e}")
        sys.exit(1)  # Quitte le programme en cas d'erreur

if __name__ == "__main__":
    initialize_ngrok()
