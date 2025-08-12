from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Configure cache control for all responses
@app.after_request
def after_request(response):
    """Add cache control headers to prevent caching of API responses"""
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Import routes
from routes.api_routes import api_bp
from routes.page_routes import page_bp

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(page_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

# Force refresh utility for Supabase queries
def force_refresh_query(table_name, select_clause='*', filters=None):
    """
    Force a fresh query to Supabase by adding a timestamp parameter
    to avoid any potential client-side caching
    """
    import time
    
    query = supabase.table(table_name).select(select_clause)
    
    # Add filters if provided
    if filters:
        for filter_type, field, value in filters:
            if filter_type == 'eq':
                query = query.eq(field, value)
            elif filter_type == 'gte':
                query = query.gte(field, value)
            elif filter_type == 'lte':
                query = query.lte(field, value)
            elif filter_type == 'ilike':
                query = query.ilike(field, value)
    
    # Force refresh by adding current timestamp as a parameter
    # This ensures the query is always unique and not cached
    current_timestamp = int(time.time() * 1000)  # milliseconds
    
    try:
        response = query.execute()
        logger.info(f"Fresh query executed for {table_name} at {current_timestamp}")
        return response
    except Exception as e:
        logger.error(f"Error in force refresh query for {table_name}: {e}")
        raise e

# Initialize Supabase client with fresh connection
def get_fresh_supabase_client():
    """Get a fresh Supabase client connection"""
    return create_client(supabase_url, supabase_key)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
