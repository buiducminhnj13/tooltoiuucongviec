import random
import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ProductTrend:
    name: str
    trend_score: int
    saturation: str  # 'Low', 'Medium', 'High', 'Very High'
    suggested_action: str
    tiktok_signals: Dict[str, Any]
    fb_signals: Dict[str, Any]
    shopee_signals: Dict[str, Any]
    last_updated: datetime.datetime

class TikTokScanner:
    """Mock TikTok trend scanner"""
    def scan_trends(self) -> List[Dict[str, Any]]:
        # Mock data - in real implementation, use TikTok API
        products = [
            {"name": "Neck Fan", "video_views_growth": 85, "creator_mentions": 12, "buy_comments": 45, "hashtag_trend": True, "shop_hot": True},
            {"name": "Car Vacuum", "video_views_growth": 72, "creator_mentions": 8, "buy_comments": 32, "hashtag_trend": False, "shop_hot": True},
            {"name": "Mini Printer", "video_views_growth": 35, "creator_mentions": 3, "buy_comments": 12, "hashtag_trend": False, "shop_hot": False},
            {"name": "Wireless Earbuds", "video_views_growth": 91, "creator_mentions": 18, "buy_comments": 67, "hashtag_trend": True, "shop_hot": True},
            {"name": "Phone Stand", "video_views_growth": 68, "creator_mentions": 9, "buy_comments": 28, "hashtag_trend": True, "shop_hot": False},
        ]
        return products

class FacebookAdsScanner:
    """Mock Facebook Ads Library scanner"""
    def scan_ads(self) -> List[Dict[str, Any]]:
        # Mock data - in real implementation, use Facebook Marketing API
        products = [
            {"name": "Neck Fan", "running_days": 15, "pages_running": 8, "creative_changes": 5, "copy_variations": 12},
            {"name": "Car Vacuum", "running_days": 22, "pages_running": 15, "creative_changes": 8, "copy_variations": 20},
            {"name": "Mini Printer", "running_days": 5, "pages_running": 2, "creative_changes": 1, "copy_variations": 3},
            {"name": "Wireless Earbuds", "running_days": 18, "pages_running": 12, "creative_changes": 7, "copy_variations": 15},
            {"name": "Phone Stand", "running_days": 12, "pages_running": 6, "creative_changes": 4, "copy_variations": 8},
        ]
        return products

class ShopeeScanner:
    """Mock Shopee PH scanner"""
    def scan_products(self) -> List[Dict[str, Any]]:
        # Mock data - in real implementation, use Shopee Open API
        products = [
            {"name": "Neck Fan", "sold_growth": 78, "review_growth": 65, "top_mover": True, "avg_price": 25, "vouchers": 8},
            {"name": "Car Vacuum", "sold_growth": 55, "review_growth": 48, "top_mover": False, "avg_price": 45, "vouchers": 5},
            {"name": "Mini Printer", "sold_growth": 25, "review_growth": 18, "top_mover": False, "avg_price": 80, "vouchers": 2},
            {"name": "Wireless Earbuds", "sold_growth": 82, "review_growth": 71, "top_mover": True, "avg_price": 35, "vouchers": 12},
            {"name": "Phone Stand", "sold_growth": 42, "review_growth": 35, "top_mover": False, "avg_price": 15, "vouchers": 4},
        ]
        return products

class TrendAnalyzer:
    def __init__(self):
        self.tiktok_scanner = TikTokScanner()
        self.fb_scanner = FacebookAdsScanner()
        self.shopee_scanner = ShopeeScanner()

    def calculate_trend_score(self, tiktok_data: Dict, fb_data: Dict, shopee_data: Dict) -> int:
        """Calculate trend score based on multiple signals"""
        score = 0

        # TikTok signals (max 25 points)
        if tiktok_data.get('video_views_growth', 0) > 70:
            score += 15
        if tiktok_data.get('creator_mentions', 0) > 10:
            score += 5
        if tiktok_data.get('buy_comments', 0) > 40:
            score += 5

        # Facebook signals (max 25 points)
        if fb_data.get('running_days', 0) > 10:
            score += 10
        if fb_data.get('pages_running', 0) > 5:
            score += 8
        if fb_data.get('creative_changes', 0) > 3:
            score += 7

        # Shopee signals (max 30 points)
        if shopee_data.get('sold_growth', 0) > 60:
            score += 15
        if shopee_data.get('review_growth', 0) > 50:
            score += 8
        if shopee_data.get('top_mover', False):
            score += 7

        # Additional factors (max 20 points)
        if shopee_data.get('vouchers', 0) > 5:
            score += 10  # Good margin indicator
        if score < 50:  # Low saturation for new products
            score += 10

        return min(score, 100)  # Cap at 100

    def determine_saturation(self, score: int, fb_pages: int, shopee_reviews: int) -> str:
        """Determine market saturation level"""
        if fb_pages > 10 and shopee_reviews > 60:
            return "Very High"
        elif fb_pages > 5 and shopee_reviews > 40:
            return "High"
        elif score > 70:
            return "Medium"
        else:
            return "Low"

    def suggest_action(self, score: int, saturation: str) -> str:
        """Suggest next action based on score and saturation"""
        if saturation == "Very High":
            return "Skip - Too saturated"
        elif saturation == "High":
            return "Test new angle"
        elif score >= 80:
            return "Test ngay"
        elif score >= 60:
            return "Monitor closely"
        else:
            return "Wait for more signals"

    def scan_all_platforms(self) -> List[ProductTrend]:
        """Main scanning function that combines all platforms"""
        tiktok_data = self.tiktok_scanner.scan_trends()
        fb_data = self.fb_scanner.scan_ads()
        shopee_data = self.shopee_scanner.scan_products()

        # Create lookup dictionaries
        tiktok_lookup = {p['name']: p for p in tiktok_data}
        fb_lookup = {p['name']: p for p in fb_data}
        shopee_lookup = {p['name']: p for p in shopee_data}

        # Get all unique product names
        all_products = set(tiktok_lookup.keys()) | set(fb_lookup.keys()) | set(shopee_lookup.keys())

        trends = []
        for product_name in all_products:
            tiktok = tiktok_lookup.get(product_name, {})
            fb = fb_lookup.get(product_name, {})
            shopee = shopee_lookup.get(product_name, {})

            score = self.calculate_trend_score(tiktok, fb, shopee)
            saturation = self.determine_saturation(score, fb.get('pages_running', 0), shopee.get('review_growth', 0))
            action = self.suggest_action(score, saturation)

            trend = ProductTrend(
                name=product_name,
                trend_score=score,
                saturation=saturation,
                suggested_action=action,
                tiktok_signals=tiktok,
                fb_signals=fb,
                shopee_signals=shopee,
                last_updated=datetime.datetime.now()
            )
            trends.append(trend)

        # Sort by trend score descending
        trends.sort(key=lambda x: x.trend_score, reverse=True)
        return trends

# Global instance for the web app
trend_analyzer = TrendAnalyzer()