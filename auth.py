"""
Authentication module for FitAI
Handles login and registration using users.json
"""
import json
import os


USERS_FILE = "users.json"


def load_users() -> dict:
    """
    Load users from JSON file
    
    Returns:
        Dictionary containing users
    """
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"users": []}


def save_users(data: dict) -> bool:
    """
    Save users to JSON file
    
    Args:
        data: Dictionary with users to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False


def register_user(username: str, password: str) -> tuple:
    """
    Register a new user
    
    Args:
        username: Username
        password: Password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not username or not password:
        return False, "Username and password are required."
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    
    data = load_users()
    
    # Check if username exists
    for user in data.get("users", []):
        if user.get("username", "").lower() == username.lower():
            return False, "Username already exists."
    
    # Default progress profile
    default_profile = {
        "goals": None,
        "weight_history": [],
        "workouts_log": [],
        "streak_days": 0,
        "total_workouts": 0,
        "start_date": None
    }
    
    # Add new user with profile
    new_user = {
        "username": username,
        "password": password,
        "profile": default_profile
    }
    
    if "users" not in data:
        data["users"] = []
    
    data["users"].append(new_user)
    
    if save_users(data):
        return True, "Registration successful! Please login."
    else:
        return False, "Error saving user data."


def login_user(username: str, password: str) -> tuple:
    """
    Authenticate user login
    
    Args:
        username: Username
        password: Password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not username or not password:
        return False, "Username and password are required."
    
    data = load_users()
    
    # Check credentials
    for user in data.get("users", []):
        if (user.get("username", "").lower() == username.lower() and 
            user.get("password") == password):
            return True, "Login successful!"
    
    return False, "Invalid username or password."


def get_user_data(username: str):
    """
    Get user data including progress profile
    
    Args:
        username: Username
        
    Returns:
        User dict or None if not found. Ensures profile exists.
    """
    data = load_users()
    for user in data.get("users", []):
        if user.get("username", "").lower() == username.lower():
            if "profile" not in user:
                user["profile"] = {
                    "goals": None,
                    "weight_history": [],
                    "workouts_log": [],
                    "streak_days": 0,
                    "total_workouts": 0,
                    "start_date": None
                }
                save_users(data)
            return user
    return None


def update_user_profile(username: str, profile: dict) -> bool:
    """
    Update entire user profile (e.g., after logging workout).
    
    Args:
        username: Username
        profile: Full updated profile dict
        
    Returns:
        True if successful
    """
    data = load_users()
    for user in data.get("users", []):
        if user.get("username", "").lower() == username.lower():
            user["profile"] = profile
            return save_users(data)
    return False
