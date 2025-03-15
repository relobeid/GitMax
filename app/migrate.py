import psycopg2
import logging
from app.utils.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

def migrate_database():
    """
    Run database migrations to update the schema.
    """
    try:
        # Parse the PostgreSQL connection string
        # Format: postgresql://username:password@host:port/database
        db_url = settings.database_url
        
        # Connect to the database
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if github_token column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'github_token'
        """)
        column_exists = cursor.fetchone() is not None
        
        # Add github_token column if it doesn't exist
        if not column_exists:
            logger.info("Adding github_token column to users table")
            cursor.execute("ALTER TABLE users ADD COLUMN github_token TEXT")
            logger.info("Migration completed successfully")
        else:
            logger.info("github_token column already exists, skipping migration")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Error during database migration: {str(e)}")
        return False

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run migrations
    success = migrate_database()
    
    if success:
        print("Database migration completed successfully")
    else:
        print("Database migration failed") 