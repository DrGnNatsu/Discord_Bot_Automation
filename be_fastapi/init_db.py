import logging
import sqlite3

from app.db.session import Base, engine
import app.models  # CRITICAL: This imports your models so Base.metadata knows about them

# filename to form database
file = "database/guild_flow.db"


logger = logging.getLogger(__name__)

try:
    conn = sqlite3.connect(file)
    print("Database formed.")
except Exception as e:
    logger.error(f"Initialise database unsuccessfully: {str(e)}")


print("Creating database tables...")
    # This line looks at all models imported above and creates the SQL tables
Base.metadata.create_all(bind=engine)
print("✅ Database 'guild_flow.db' created successfully!")