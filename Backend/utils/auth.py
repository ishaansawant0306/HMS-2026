"""
Authentication utilities for password hashing and verification
"""
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException


def hash_password(password):
    """
    Hash a password using werkzeug's security functions.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(hashed_password, password):
    """
    Verify a password against its hash.
    
    Args:
        hashed_password (str): The hashed password from database
        password (str): The plain text password to verify
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(hashed_password, password)


def require_role(*allowed_roles):
    """
    Decorator to enforce role-based access control.
    
    Args:
        *allowed_roles: Variable number of role names (e.g., 'admin', 'doctor', 'patient')
        
    Returns:
        function: Decorated function that checks roles
        
    Example:
        @require_role('admin', 'doctor')
        def some_endpoint():
            return "Access granted"
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except JWTExtendedException as e:
                return jsonify({"msg": "Token verification failed", "error": str(e)}), 401
            
            # Get user identity from JWT token
            from models import User
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({"msg": "User not found"}), 404
            
            if user.role not in allowed_roles:
                return jsonify({"msg": f"Unauthorized. Required roles: {', '.join(allowed_roles)}"}), 403
            
            # User is authorized, proceed with the function
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def require_auth():
    """
    Decorator to require JWT authentication (any authenticated user).
    
    Returns:
        function: Decorated function that checks JWT
        
    Example:
        @require_auth()
        def protected_endpoint():
            return "You are authenticated"
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except JWTExtendedException as e:
                return jsonify({"msg": "Token verification failed", "error": str(e)}), 401
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator
