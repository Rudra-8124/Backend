import logging
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

# Ensure environment variables exist before attempting to create the client
if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment variables.")

try:
    # Initialize the Supabase client
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    raise e

def insert_data(table: str, data: dict) -> dict:
    """
    Inserts a record into the specified table.
    """
    try:
        response = supabase.table(table).insert(data).execute()
        if len(response.data) > 0:
            return response.data[0]
        return {}
    except Exception as e:
        logger.error(f"Error inserting data into {table}: {e}")
        raise ValueError(f"Database insert error: {e}")

def fetch_data(table: str, filters: dict = None) -> list:
    """
    Fetches records from the table, optionally applying an equality filter.
    """
    try:
        query = supabase.table(table).select("*")
        
        # Apply strict equality filters dynamically if provided
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
                
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching data from {table}: {e}")
        raise ValueError(f"Database fetch error: {e}")

def update_data(table: str, record_id: str, data: dict) -> dict:
    """
    Updates a specfic record by id.
    """
    try:
        response = supabase.table(table).update(data).eq('id', record_id).execute()
        if len(response.data) > 0:
            return response.data[0]
        return {}
    except Exception as e:
        logger.error(f"Error updating data in {table}: {e}")
        raise ValueError(f"Database update error: {e}")

def delete_data(table: str, record_id: str) -> dict:
    """
    Deletes a specific record by id.
    """
    try:
        response = supabase.table(table).delete().eq('id', record_id).execute()
        if len(response.data) > 0:
            return response.data[0]
        return {}
    except Exception as e:
        logger.error(f"Error deleting data from {table}: {e}")
        raise ValueError(f"Database delete error: {e}")
