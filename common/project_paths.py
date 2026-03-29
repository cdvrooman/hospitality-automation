from pathlib import Path

def get_project_root() -> Path:
    """
    Identifies the project root by searching for a marker (.env or .git).
    Ensures path consistency when running automation from subdirectories.
    """
    # Start at the directory containing this utility
    current_path = Path(__file__).resolve().parent
    
    # Climb the directory tree to find the root marker
    for parent in [current_path] + list(current_path.parents):
        if (parent / ".env").exists() or (parent / ".git").exists():
            return parent
            
    # Fallback to the script's own directory if no marker is found
    return current_path