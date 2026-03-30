"""
Salta Hospitality Automation - Common Utilities Package
Centralized constants and environment validation for:
- Casa Kolla (Property Management & Expansion)
- Zoho CRM / Deluge / HubSpot STR Club Integration
- SmartThings Edge / Raspberry Pi Local-First IoT
"""

# --- EXPOSED UTILITIES (Simplified Imports) ---
from .project_paths import get_project_root
from .database import get_db_cursor
from .config import (
    TIMEZONE, 
    PROJECT_NAME,
    AI_TEMP_PRECISE,
    AI_TEMP_CREATIVE,
    AI_MODELS,
    DEFAULT_DB_NAME
)

# Defining exports for 'from common import *'
__all__ = [
    'get_project_root', 
    'get_db_cursor', 
    'TIMEZONE', 
    'PROJECT_NAME',
    'AI_TEMP_PRECISE',
    'AI_TEMP_CREATIVE',
    'AI_MODELS',
    'DEFAULT_DB_NAME'
]