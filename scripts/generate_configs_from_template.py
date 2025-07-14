#!/usr/bin/env python3
"""
Generate bot configurations from template
This script creates individual bot config files from the template
"""

import json
import secrets
import string
from pathlib import Path

def generate_jwt_secret():
    """Generate a secure JWT secret (64 characters)"""
    return secrets.token_hex(32)

def generate_ws_token():
    """Generate a secure WebSocket token (32 characters)"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def generate_bot_config(bot_id, template_config):
    """Generate configuration for a specific bot"""
    config = template_config.copy()
    
    # Update bot-specific values
    config['api_server']['jwt_secret_key'] = generate_jwt_secret()
    config['api_server']['ws_token'] = generate_ws_token()
    config['api_server']['password'] = f'bot{bot_id:02d}pass'
    config['bot_name'] = f'freqtrade-bot-{bot_id:02d}'
    config['db_url'] = f'sqlite:///user_data/tradesv3-bot-{bot_id:02d}.sqlite'
    
    return config

def main():
    """Generate configurations for all 12 bots"""
    template_file = Path(__file__).parent.parent / 'configs' / 'config-template.json'
    configs_dir = Path(__file__).parent.parent / 'configs'
    
    # Load template
    with open(template_file, 'r') as f:
        template_config = json.load(f)
    
    # Generate configurations for all 12 bots
    for i in range(1, 13):
        config = generate_bot_config(i, template_config)
        config_file = configs_dir / f'config-bot-{i:02d}.json'
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Generated config for bot {i:02d}")
    
    print("All bot configurations generated successfully!")
    print("\nIMPORTANT:")
    print("1. Update exchange API keys and secrets in the config files")
    print("2. Set dry_run: false when ready for live trading")
    print("3. Review and adjust trading parameters as needed")

if __name__ == '__main__':
    main()