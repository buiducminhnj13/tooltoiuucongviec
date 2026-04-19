from flask import Flask, render_template, send_from_directory
import os
from trend_scanner import trend_analyzer

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")

app = Flask(__name__, static_folder='product-optimizer-website', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('product-optimizer-website', 'index.html')

@app.route('/trends')
def trends_dashboard():
    trends = trend_analyzer.scan_all_platforms()
    return render_template('trends.html', trends=trends)

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('product-optimizer-website', path)

@app.errorhandler(404)
def not_found(error):
    return send_from_directory('product-optimizer-website', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
