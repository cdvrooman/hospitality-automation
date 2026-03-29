"""
Database Management Utility - Salta Hospitality Automation
Currently using SQLite for local-first reliability.
Designed for a future migration to PostgreSQL or a similar 
Pi-friendly RDBMS without breaking implementation logic.
"""

import sqlite3
import os
from contextlib import contextmanager
from .project_paths import get_project_root

# --- 1. CONFIGURATION ---
# Defaulting to a local file in the project root for now.
# This path can be overridden by a 'CASA_KOLLA_DB_PATH' env variable.
DEFAULT_DB_NAME = "casa_kolla_management.sqlite"
DB_PATH = os.getenv("CASA_KOLLA_DB_PATH", os.path.join(get_project_root(), DEFAULT_DB_NAME))

# --- 2. THE INTERFACE ---
@contextmanager
def get_db_cursor():
    """
    Context manager for database operations.
    Handles connection, cursor creation, and automatic commits/rollback.
    
    Usage:
        from common.database import get_db_cursor
        with get_db_cursor() as cur:
            cur.execute("SELECT * FROM Units")
    """
    conn = sqlite3.connect(DB_PATH)
    # Enabling Row factory allows accessing columns by name: row['unit_name']
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[DATABASE ERROR] Transaction failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()

# --- 3. INITIALIZATION ---
def initialize_schema():
    """
    Sets up the core tables for the STR units.
    This can be run once to 'bootstrap' the local Raspberry Pi environment.
    """
    with get_db_cursor() as cur:
        # Core Table: Inventory Units for Casa Kolla (Rooms & Apartments)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_name TEXT UNIQUE NOT NULL,
                smart_lock_id TEXT,
                status TEXT DEFAULT 'available'
            )
        ''')