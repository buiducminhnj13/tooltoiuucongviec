#!/usr/bin/env python3
"""
Facebook API Test Script
Test Facebook Ads Library API connection and functionality
"""

import os
import requests
from datetime import datetime, timedelta
import json

class FacebookAPITester:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')

    def test_basic_connection(self):
        """Test basic API connection"""
        print("🔍 Testing basic Facebook API connection...")

        if not self.access_token:
            print("❌ FACEBOOK_ACCESS_TOKEN not found in environment")
            return False

        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}

            response = requests.get(url, params=params)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected successfully as: {user_data.get('name', 'Unknown')}")
                return True
            else:
                error_data = response.json()
                print(f"❌ API Error: {error_data}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def test_ads_library_access(self):
        """Test access to Ads Library"""
        print("\n📊 Testing Ads Library access...")

        if not self.access_token:
            return False

        try:
            # Test with a simple search
            url = f"{self.base_url}/ads_archive"
            params = {
                'access_token': self.access_token,
                'search_terms': 'neck fan',
                'ad_type': 'ALL',
                'ad_active_status': 'ALL',
                'fields': 'id,campaign_name,adset_name,status',
                'limit': 5
            }

            response = requests.get(url, params=params)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                ads_data = response.json()
                ad_count = len(ads_data.get('data', []))
                print(f"✅ Ads Library accessible! Found {ad_count} ads for 'neck fan'")

                if ad_count > 0:
                    print("📋 Sample ad data:")
                    for ad in ads_data['data'][:2]:
                        print(f"   • Campaign: {ad.get('campaign_name', 'N/A')}")
                        print(f"   • Status: {ad.get('status', 'N/A')}")

                return True
            else:
                error_data = response.json()
                print(f"❌ Ads Library Error: {error_data}")

                # Check for common issues
                if 'error' in error_data:
                    error_code = error_data['error'].get('code')
                    if error_code == 190:
                        print("💡 Token expired or invalid")
                    elif error_code == 200:
                        print("💡 Permission denied - check ads_read scope")

                return False

        except Exception as e:
            print(f"❌ Ads Library test error: {e}")
            return False

    def test_token_info(self):
        """Get detailed token information"""
        print("\n🔑 Testing token information...")

        if not self.access_token:
            return False

        try:
            url = f"{self.base_url}/debug_token"
            params = {
                'input_token': self.access_token,
                'access_token': self.access_token
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                token_data = response.json().get('data', {})
                print("✅ Token Information:")
                print(f"   • App ID: {token_data.get('app_id', 'N/A')}")
                print(f"   • User ID: {token_data.get('user_id', 'N/A')}")
                print(f"   • Expires: {token_data.get('expires_at', 'Never')}")
                print(f"   • Valid: {token_data.get('is_valid', False)}")

                scopes = token_data.get('scopes', [])
                print(f"   • Scopes: {', '.join(scopes)}")

                if 'ads_read' not in scopes:
                    print("⚠️  WARNING: ads_read scope not found!")
                    print("   💡 You need ads_read permission for Ads Library access")

                return True
            else:
                print(f"❌ Token debug failed: {response.json()}")
                return False

        except Exception as e:
            print(f"❌ Token info error: {e}")
            return False

    def run_full_test(self):
        """Run complete API test suite"""
        print("🚀 FACEBOOK API TEST SUITE")
        print("=" * 50)

        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Loaded .env file")
        except ImportError:
            print("⚠️  python-dotenv not installed")

        # Check credentials
        print("\n📋 Credentials Status:")
        print(f"   • Access Token: {'✅ SET' if self.access_token else '❌ NOT SET'}")
        print(f"   • App ID: {'✅ SET' if self.app_id else '❌ NOT SET'}")
        print(f"   • App Secret: {'✅ SET' if self.app_secret else '❌ NOT SET'}")

        if not all([self.access_token, self.app_id, self.app_secret]):
            print("\n❌ Missing credentials! Please set them in .env file first.")
            return False

        # Run tests
        basic_ok = self.test_basic_connection()
        token_ok = self.test_token_info()
        ads_ok = self.test_ads_library_access()

        print("\n" + "=" * 50)
        print("📊 TEST RESULTS:")
        print(f"   • Basic Connection: {'✅ PASS' if basic_ok else '❌ FAIL'}")
        print(f"   • Token Info: {'✅ PASS' if token_ok else '❌ FAIL'}")
        print(f"   • Ads Library: {'✅ PASS' if ads_ok else '❌ FAIL'}")

        if all([basic_ok, token_ok, ads_ok]):
            print("\n🎉 ALL TESTS PASSED! Facebook API is ready to use!")
            return True
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
            return False

def main():
    tester = FacebookAPITester()
    success = tester.run_full_test()

    if not success:
        print("\n" + "=" * 50)
        print("🛠️  SETUP HELP:")
        print("1. Go to https://developers.facebook.com/apps/")
        print("2. Create a new app or use existing one")
        print("3. Add 'Marketing API' product")
        print("4. Generate access token with 'ads_read' permission")
        print("5. Copy App ID and App Secret")
        print("6. Update .env file with the credentials")
        print("7. Run this test again")

if __name__ == "__main__":
    main()