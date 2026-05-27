import sqlite3
from contextlib import contextmanager

# This is the physical file that will be created on your hard drive.
# The new, rebranded database file
DATABASE_FILE = "logistics_manager.db"

def initialize_database():
    """
    Bootstraps the database. It checks if the tables exist, 
    and if they don't, it creates them.
    """
    # Open a connection stream to the database file
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # TABLE 1: Active Deliveries (Currently on the road)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_deliveries (
            trip_id TEXT PRIMARY KEY,
            sequence_string TEXT NOT NULL,
            total_weight REAL NOT NULL,
            status TEXT DEFAULT 'IN-TRANSIT'
        )
    ''')

    # TABLE 2: Completed Deliveries (Historical Archive)
    # We add a 'completion_time' column here to track exactly when it finished.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_deliveries (
            trip_id TEXT PRIMARY KEY,
            sequence_string TEXT NOT NULL,
            total_weight REAL NOT NULL,
            completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'ARCHIVED SUCCESS'
        )
    ''')

    # Save (commit) the structural changes and close the connection
    conn.commit()
    conn.close()
    print("Logistics Database initialized successfully.")


@contextmanager
def get_db_connection():
    """
    A memory-safe generator for database connections.
    This ensures that even if the server crashes during a read/write,
    the database file lock is safely released.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    # This setting tells SQLite to return rows as dictionaries instead of raw tuples,
    # making it much easier to convert the data into JSON later.
    conn.row_factory = sqlite3.Row 
    try:
        yield conn
    finally:
        conn.close()