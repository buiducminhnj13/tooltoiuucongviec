import os
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time

class RealTikTokScanner:
    """Real TikTok API implementation using TikTok for Developers"""

    def __init__(self):
        self.base_url = "https://open-api.tiktok.com"
        self.client_key = os.getenv('TIKTOK_CLIENT_KEY')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
        self.access_token = None

    def authenticate(self) -> bool:
        """Get access token from TikTok"""
        if not self.client_key or not self.client_secret:
            print("❌ TikTok API credentials not found")
            return False

        try:
            url = f"{self.base_url}/oauth/access_token/"
            data = {
                'client_key': self.client_key,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                return True
            else:
                print(f"❌ TikTok auth failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ TikTok auth error: {e}")
            return False

    def search_hashtags(self, hashtag: str) -> Dict[str, Any]:
        """Search for trending hashtags and related content"""
        if not self.access_token:
            return {}

        try:
            url = f"{self.base_url}/research/video/query/"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            params = {
                'query': f'#{hashtag}',
                'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y%m%d'),
                'end_date': datetime.now().strftime('%Y%m%d')
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    'hashtag': hashtag,
                    'video_count': data.get('video_count', 0),
                    'total_views': data.get('total_views', 0),
                    'avg_views': data.get('avg_views', 0)
                }
            return {}
        except Exception as e:
            print(f"❌ TikTok hashtag search error: {e}")
            return {}

    def get_trending_products(self) -> List[Dict[str, Any]]:
        """Get trending products from TikTok Shop"""
        if not self.access_token:
            return []

        try:
            # This would use TikTok Shop API
            # For now, return mock data structure
            trending_hashtags = ['neckfan', 'carvacuum', 'wirelessearbuds', 'phonestand', 'miniprinter']

            products = []
            for hashtag in trending_hashtags:
                hashtag_data = self.search_hashtags(hashtag)
                if hashtag_data:
                    products.append({
                        'name': hashtag.title(),
                        'video_views_growth': min(hashtag_data.get('avg_views', 0) // 1000, 100),
                        'creator_mentions': hashtag_data.get('video_count', 0) // 10,
                        'buy_comments': hashtag_data.get('video_count', 0) // 20,
                        'hashtag_trend': True,
                        'shop_hot': hashtag_data.get('total_views', 0) > 100000
                    })
            return products
        except Exception as e:
            print(f"❌ TikTok trending products error: {e}")
            return []

class RealFacebookAdsScanner:
    """Real Facebook Ads Library API implementation"""

    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')

    def authenticate(self) -> bool:
        """Verify Facebook access token"""
        if not self.access_token:
            print("❌ Facebook access token not found")
            return False

        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                print("✅ Facebook authentication successful")
                return True
            else:
                print(f"❌ Facebook auth failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Facebook auth error: {e}")
            return False

    def search_ads(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search Facebook Ads Library for product campaigns"""
        if not self.access_token:
            return []

        results = []
        for term in search_terms:
            try:
                url = f"{self.base_url}/ads_archive"
                params = {
                    'access_token': self.access_token,
                    'search_terms': term,
                    'ad_type': 'ALL',
                    'ad_active_status': 'ALL',
                    'fields': 'id,campaign_name,adset_name,created_time,updated_time,status,spend,impressions,clicks',
                    'limit': 50
                }

                response = requests.get(url, params=params)
                if response.status_code == 200:
                    ads_data = response.json().get('data', [])

                    # Analyze ads for this product
                    active_ads = [ad for ad in ads_data if ad.get('status') == 'ACTIVE']
                    recent_ads = [ad for ad in active_ads if self._is_recent(ad.get('created_time', ''))]

                    if recent_ads:
                        results.append({
                            'name': term.title(),
                            'running_days': len(set(ad.get('created_time', '').split('T')[0] for ad in recent_ads)),
                            'pages_running': len(set(ad.get('campaign_name', '') for ad in recent_ads)),
                            'creative_changes': len(recent_ads),
                            'copy_variations': len(set(ad.get('adset_name', '') for ad in recent_ads))
                        })

                time.sleep(1)  # Rate limiting

            except Exception as e:
                print(f"❌ Facebook ads search error for {term}: {e}")

        return results

    def _is_recent(self, date_str: str) -> bool:
        """Check if ad was created within last 30 days"""
        try:
            ad_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return (datetime.now(ad_date.tzinfo) - ad_date).days <= 30
        except:
            return False

class RealShopeeScanner:
    """Real Shopee Open Platform API implementation"""

    def __init__(self):
        self.base_url = "https://partner.shopeemobile.com/api/v2"
        self.partner_id = os.getenv('SHOPEE_PARTNER_ID')
        self.partner_key = os.getenv('SHOPEE_PARTNER_KEY')
        self.shop_id = os.getenv('SHOPEE_SHOP_ID')
        self.access_token = None

    def authenticate(self) -> bool:
        """Get Shopee access token"""
        if not all([self.partner_id, self.partner_key, self.shop_id]):
            print("❌ Shopee API credentials not found")
            return False

        try:
            # Shopee authentication flow
            # This is simplified - real implementation needs proper OAuth flow
            url = f"{self.base_url}/auth/access_token/get"
            timestamp = str(int(time.time()))

            # Create signature (simplified)
            base_string = f"{self.partner_id}{url.split('/')[-1]}{timestamp}"
            # In real implementation, use HMAC-SHA256 with partner_key

            data = {
                'partner_id': self.partner_id,
                'shop_id': self.shop_id,
                'timestamp': timestamp
            }

            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                return True
            else:
                print(f"❌ Shopee auth failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Shopee auth error: {e}")
            return False

    def get_product_sales(self, product_ids: List[str]) -> List[Dict[str, Any]]:
        """Get sales data for products"""
        if not self.access_token:
            return []

        results = []
        for product_id in product_ids:
            try:
                url = f"{self.base_url}/product/get_item_base_info"
                headers = {'Authorization': f'Bearer {self.access_token}'}
                params = {
                    'partner_id': self.partner_id,
                    'shop_id': self.shop_id,
                    'item_id': product_id,
                    'timestamp': str(int(time.time()))
                }

                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    item_data = response.json()['item']

                    # Get sales performance (would need additional API calls)
                    results.append({
                        'name': item_data.get('item_name', ''),
                        'sold_growth': 0,  # Would calculate from historical data
                        'review_growth': item_data.get('cmt_count', 0),
                        'top_mover': False,  # Would check category rankings
                        'avg_price': float(item_data.get('price', 0)),
                        'vouchers': len(item_data.get('voucher_info', []))
                    })

                time.sleep(1)  # Rate limiting

            except Exception as e:
                print(f"❌ Shopee product data error for {product_id}: {e}")

        return results

# Configuration for API credentials
API_CONFIG = {
    'tiktok': {
        'client_key': 'TIKTOK_CLIENT_KEY',
        'client_secret': 'TIKTOK_CLIENT_SECRET',
        'docs': 'https://developers.tiktok.com/products/research-api/'
    },
    'facebook': {
        'access_token': 'FACEBOOK_ACCESS_TOKEN',
        'app_id': 'FACEBOOK_APP_ID',
        'app_secret': 'FACEBOOK_APP_SECRET',
        'docs': 'https://developers.facebook.com/docs/marketing-api/'
    },
    'shopee': {
        'partner_id': 'SHOPEE_PARTNER_ID',
        'partner_key': 'SHOPEE_PARTNER_KEY',
        'shop_id': 'SHOPEE_SHOP_ID',
        'docs': 'https://open.shopee.com/documents?module=2&type=1&id=66'
    }
}

def setup_environment_variables():
    """Guide for setting up environment variables"""
    print("🔧 CÀI ĐẶT BIẾN MÔI TRƯỜNG:")
    print("=" * 50)

    for platform, config in API_CONFIG.items():
        print(f"\n📱 {platform.upper()}:")
        print(f"   📖 Docs: {config['docs']}")

        for env_var in config.values():
            if isinstance(env_var, str) and env_var.startswith(platform.upper()):
                print(f"   • {env_var}")

    print("\n💡 Cách thiết lập:")
    print("   1. Tạo file .env trong thư mục project")
    print("   2. Thêm các biến trên với giá trị thực")
    print("   3. Load file .env trong code (sử dụng python-dotenv)")
    print("\n⚠️  Lưu ý: KHÔNG commit file .env lên GitHub!")