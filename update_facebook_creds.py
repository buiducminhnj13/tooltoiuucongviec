#!/usr/bin/env python3
"""
Quick .env updater for Facebook API credentials
"""

import os
from pathlib import Path

def update_env_file():
    """Update .env file with Facebook credentials"""

    env_file = Path('.env')

    # Create .env if it doesn't exist
    if not env_file.exists():
        print("📄 Creating .env file...")
        env_file.write_text("""# Facebook API Credentials
FACEBOOK_ACCESS_TOKEN=your_access_token_here
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here

# TikTok API Credentials
TIKTOK_CLIENT_KEY=your_tiktok_client_key_here
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret_here

# Shopee API Credentials
SHOPEE_PARTNER_ID=your_shopee_partner_id_here
SHOPEE_PARTNER_KEY=your_shopee_partner_key_here
SHOPEE_SHOP_ID=your_shopee_shop_id_here
""")

    print("🔑 FACEBOOK API CREDENTIALS SETUP")
    print("=" * 40)

    # Get current values
    current_token = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    current_app_id = os.getenv('FACEBOOK_APP_ID', '')
    current_app_secret = os.getenv('FACEBOOK_APP_SECRET', '')

    print(f"Current Access Token: {'***' + current_token[-10:] if current_token else 'NOT SET'}")
    print(f"Current App ID: {current_app_id or 'NOT SET'}")
    print(f"Current App Secret: {'***' + current_app_secret[-5:] if current_app_secret else 'NOT SET'}")
    print()

    # Ask for new values
    print("Enter your Facebook API credentials (press Enter to keep current):")

    new_token = input("Access Token: ").strip()
    if not new_token and not current_token:
        print("❌ Access Token is required!")
        return False

    new_app_id = input("App ID: ").strip()
    if not new_app_id and not current_app_id:
        print("❌ App ID is required!")
        return False

    new_app_secret = input("App Secret: ").strip()
    if not new_app_secret and not current_app_secret:
        print("❌ App Secret is required!")
        return False

    # Update .env file
    env_content = env_file.read_text()

    # Update each credential
    if new_token:
        if 'FACEBOOK_ACCESS_TOKEN=' in env_content:
            env_content = env_content.replace(
                f"FACEBOOK_ACCESS_TOKEN={current_token}",
                f"FACEBOOK_ACCESS_TOKEN={new_token}"
            )
        else:
            env_content += f"\nFACEBOOK_ACCESS_TOKEN={new_token}"

    if new_app_id:
        if 'FACEBOOK_APP_ID=' in env_content:
            env_content = env_content.replace(
                f"FACEBOOK_APP_ID={current_app_id}",
                f"FACEBOOK_APP_ID={new_app_id}"
            )
        else:
            env_content += f"\nFACEBOOK_APP_ID={new_app_id}"

    if new_app_secret:
        if 'FACEBOOK_APP_SECRET=' in env_content:
            env_content = env_content.replace(
                f"FACEBOOK_APP_SECRET={current_app_secret}",
                f"FACEBOOK_APP_SECRET={new_app_secret}"
            )
        else:
            env_content += f"\nFACEBOOK_APP_SECRET={new_app_secret}"

    # Write back to file
    env_file.write_text(env_content)

    print("\n✅ Credentials updated successfully!")
    print("🧪 Run 'python test_facebook_api.py' to test the connection")

    return True

if __name__ == "__main__":
    update_env_file()