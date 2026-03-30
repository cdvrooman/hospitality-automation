import os

# --- 1. SHARED PROJECT CONSTANTS ---
# Standardizing these across all Python scripts for consistency
TIMEZONE = "America/Argentina/Salta"
PROJECT_NAME = "Hospitality-Automation"

# --- AI TEMPERATURE SETTINGS ---
# Controls the balance between deterministic logic and creative flow.
AI_TEMP_PRECISE = 0.2  # Use for: Data extraction, chains, and logic
AI_TEMP_CREATIVE = 0.7 # Use for: Guest communication and marketing

# --- AI MODEL MAPPING ---
# Intent-based model selection to allow for easy global upgrades.
AI_MODELS = {
    "logic": "gemini-3.1-pro-preview",    # Complex reasoning (Financials/Legal)
    "speed": "gemini-3-flash-preview",  # Fast response (IoT/Guest FAQs)
    "vision": "gemini-3-flash-preview", # Image analysis (Property/ID photos)
}

# --- DATABASE SETTINGS ---
DEFAULT_DB_NAME = "casa_kolla_management.sqlite"

# --- 2. ENVIRONMENT SANITY CHECKS ---
# Critical IDs and Keys. Uncomment as they are defined in .env 
# to prevent scripts from running if the infrastructure is missing.

def _validate_environment():
    """ Internal check to ensure the environment is ready for automation. """
    required_keys = [
        # "ZOHO_CLIENT_ID",
        # "ZOHO_CLIENT_SECRET",
        # "HUBSPOT_ACCESS_TOKEN",
        # "SMARTTHINGS_API_TOKEN",
        # "CASA_KOLLA_DB_PATH",
    ]
    
    missing = [key for key in required_keys if not os.getenv(key)]
    
    if missing:
        # Using a warning to flag missing cloud/local access 
        # without killing standalone research scripts.
        print(f"--- [STATUS] Missing Environment Variables: {', '.join(missing)} ---")

# Run validation immediately upon config import
_validate_environment()
