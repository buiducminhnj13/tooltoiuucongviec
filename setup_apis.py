#!/usr/bin/env python3
"""
AI Trend Scanner - API Setup Guide
==================================

This script helps you set up API credentials for TikTok, Facebook, and Shopee
to enable real-time trend scanning instead of mock data.
"""

import os
import json
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 AI TREND SCANNER - API SETUP GUIDE")
    print("=" * 60)

def print_platform_guide(platform_name, steps, credentials, docs_url):
    print(f"\n📱 {platform_name.upper()}")
    print("-" * 40)
    print(f"📖 Documentation: {docs_url}")
    print("\n📋 Steps to get credentials:")

    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")

    print("\n🔑 Required credentials:")
    for cred in credentials:
        print(f"   • {cred}")

def create_env_file():
    """Create .env file with placeholder values"""
    env_content = """# TikTok API Credentials
# Get from: https://developers.tiktok.com/products/research-api/
TIKTOK_CLIENT_KEY=your_tiktok_client_key_here
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret_here

# Facebook API Credentials
# Get from: https://developers.facebook.com/apps/
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here

# Shopee API Credentials
# Get from: https://partner.shopee.com.ph/
SHOPEE_PARTNER_ID=your_shopee_partner_id_here
SHOPEE_PARTNER_KEY=your_shopee_partner_key_here
SHOPEE_SHOP_ID=your_shopee_shop_id_here
"""

    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with placeholder values")
        print("   📝 Edit .env file and replace placeholder values with real credentials")
    else:
        print("⚠️  .env file already exists")

def main():
    print_header()

    # TikTok setup guide
    print_platform_guide(
        "TikTok",
        [
            "Go to https://developers.tiktok.com/products/research-api/",
            "Create a developer account and app",
            "Apply for Research API access (may take time for approval)",
            "Get Client Key and Client Secret from app settings"
        ],
        ["TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET"],
        "https://developers.tiktok.com/products/research-api/"
    )

    # Facebook setup guide
    print_platform_guide(
        "Facebook",
        [
            "Go to https://developers.facebook.com/apps/",
            "Create a new app or use existing one",
            "Add Marketing API product to your app",
            "Generate access token with ads_read permission",
            "Get App ID and App Secret from app settings"
        ],
        ["FACEBOOK_ACCESS_TOKEN", "FACEBOOK_APP_ID", "FACEBOOK_APP_SECRET"],
        "https://developers.facebook.com/docs/marketing-api/"
    )

    # Shopee setup guide
    print_platform_guide(
        "Shopee Philippines",
        [
            "Go to https://partner.shopee.com.ph/",
            "Register as a Shopee Partner",
            "Create an app in the partner dashboard",
            "Get Partner ID, Partner Key, and Shop ID",
            "Apply for necessary API permissions"
        ],
        ["SHOPEE_PARTNER_ID", "SHOPEE_PARTNER_KEY", "SHOPEE_SHOP_ID"],
        "https://open.shopee.com/documents?module=2&type=1&id=66"
    )

    print("\n" + "=" * 60)
    print("🛠️  SETUP INSTRUCTIONS")
    print("=" * 60)

    print("\n1. 📄 Create .env file:")
    create_env_file()

    print("\n2. 🔧 Install required packages:")
    print("   pip install python-dotenv requests pandas numpy")

    print("\n3. 🧪 Test API connections:")
    print("   python -c \"from trend_scanner import trend_analyzer; print('APIs loaded successfully')\"")

    print("\n4. 🚀 Deploy to Railway:")
    print("   - Push code to GitHub")
    print("   - Deploy on Railway")
    print("   - Add environment variables in Railway dashboard")

    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT NOTES")
    print("=" * 60)
    print("• Never commit .env file to GitHub (it's in .gitignore)")
    print("• API rate limits apply - monitor usage")
    print("• Some APIs require manual approval")
    print("• Costs may apply for high-volume API usage")
    print("• Start with development/sandbox accounts first")

    print("\n🎯 Once setup is complete, your AI Trend Scanner will use real data!")
    print("   Visit /trends to see live trend analysis.")

if __name__ == "__main__":
    main()