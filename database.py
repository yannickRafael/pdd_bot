
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
app_config = Config()

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(
            host=app_config.DB_HOST,
            port=app_config.DB_PORT,
            dbname=app_config.DB_NAME,
            user=app_config.DB_USER,
            password=app_config.DB_PASSWORD
        )
        
        return conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e