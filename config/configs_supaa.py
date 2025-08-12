import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Initialize Supabase client
def get_supabase_client(service_key=False):
    """Get Supabase client with appropriate key"""
    try:
        key = SUPABASE_SERVICE_KEY if service_key else SUPABASE_ANON_KEY
        client: Client = create_client(SUPABASE_URL, key)
        return client
    except Exception as e:
        logger.error(f"Error creating Supabase client: {e}")
        raise

# Database helper functions
def safe_execute(client: Client, operation, *args, **kwargs):
    """Safely execute database operations with error handling"""
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        raise

def upsert_data(client: Client, table_name: str, data: dict):
    """Upsert data into a table"""
    try:
        response = client.table(table_name).upsert(data).execute()
        logger.info(f"Upserted data into {table_name}: {len(response.data)} records")
        return response
    except Exception as e:
        logger.error(f"Error upserting data into {table_name}: {e}")
        raise

def get_data(client: Client, table_name: str, filters=None):
    """Get data from a table with optional filters"""
    try:
        query = client.table(table_name).select("*")
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        response = query.execute()
        logger.info(f"Retrieved {len(response.data)} records from {table_name}")
        return response.data
    except Exception as e:
        logger.error(f"Error getting data from {table_name}: {e}")
        raise
