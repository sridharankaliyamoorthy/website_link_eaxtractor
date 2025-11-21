"""
Flask API for Link Extractor
Provides REST API endpoints for extracting links from websites.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from link_extractor import LinkExtractor

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'service': 'Link Extractor API',
        'version': '1.0.0',
        'endpoints': {
            '/api/extract': 'POST - Extract links from a URL',
            '/api/health': 'GET - Health check'
        },
        'frontend': 'Open http://localhost:8000 for the web interface',
        'api_port': 5001
    })


@app.route('/api/extract', methods=['POST'])
def extract_links():
    """Extract links from a given URL."""
    try:
        data = request.get_json()
        url = data.get('url')
        use_browser = data.get('use_browser', False)
        filter_domain = data.get('filter_domain', False)
        include_external = data.get('include_external', True)
        timeout = data.get('timeout', 10)
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }), 400
        
        extractor = LinkExtractor(url, timeout=timeout)
        
        if use_browser:
            # Use longer wait time for browser automation (15 seconds default)
            wait_time = data.get('wait_time', 15)
            links, diagnostics = extractor.extract_links_with_browser(
                filter_domain=filter_domain,
                include_external=include_external,
                wait_time=wait_time
            )
        else:
            links, diagnostics = extractor.get_all_links(
                filter_domain=filter_domain,
                include_external=include_external
            )
        
        links_list = sorted(list(links))
        
        # Check if there was an error in diagnostics
        if diagnostics.get('error'):
            return jsonify({
                'success': False,
                'error': diagnostics.get('error'),
                'links': links_list,
                'count': len(links_list),
                'diagnostics': diagnostics
            }), 400
        
        return jsonify({
            'success': True,
            'links': links_list,
            'count': len(links_list),
            'diagnostics': diagnostics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Link Extractor API'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

