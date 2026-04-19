# Facebook API Setup Guide for AI Trend Scanner
# ================================================

## 🚀 QUICK START (5 minutes)

### Step 1: Create Facebook App
1. Go to https://developers.facebook.com/apps/
2. Click "Create App"
3. Choose "Business" → "Yourself or your own business"
4. Fill in:
   - App name: "AI Trend Scanner"
   - App contact email: [your email]
   - Business account: (optional)

### Step 2: Add Marketing API
1. In your app dashboard, click "Add Product"
2. Find "Marketing API" and click "Set Up"
3. Complete the setup wizard

### Step 3: Generate Access Token
1. Go to "Marketing API" → "Tools"
2. Click "Create Access Token"
3. Select permissions: ✅ `ads_read`
4. Click "Generate Token"
5. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

### Step 4: Get App Credentials
1. Go to "Settings" → "Basic"
2. Copy:
   - App ID
   - App Secret

### Step 5: Update .env file
Edit the `.env` file in your project with the credentials:

```
FACEBOOK_ACCESS_TOKEN=your_access_token_here
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
```

### Step 6: Test Connection
Run the test script:
```bash
python test_facebook_api.py
```

## 🔧 TROUBLESHOOTING

### "Token expired" error
- Access tokens expire every 60 days
- Generate a new one following Step 3 above

### "Permission denied" error
- Make sure you selected `ads_read` permission
- Check token scopes in the test output

### "App not approved" error
- Facebook may require app review for production use
- For development/testing, short-lived tokens work

## 📊 WHAT YOU'LL GET

Once connected, your AI Trend Scanner will analyze:
- ✅ Ads running duration (>10 days = +20 points)
- ✅ Number of pages running same product
- ✅ Creative changes frequency
- ✅ Copy variations
- ✅ Campaign performance signals

## 🎯 NEXT STEPS

After Facebook API is working:
1. Test the trend scanner: Visit `/trends`
2. Add TikTok API (optional)
3. Add Shopee API (optional)
4. Deploy to Railway with environment variables

---
*Need help? Check the test script output for specific error messages.*