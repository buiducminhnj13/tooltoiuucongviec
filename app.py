from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='product-optimizer-website', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('product-optimizer-website', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('product-optimizer-website', path)

@app.errorhandler(404)
def not_found(error):
    return send_from_directory('product-optimizer-website', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
