
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException


def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

# to verify password agaist hash 
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


def require_role(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except JWTExtendedException as e:
                return jsonify({"msg": "Token verification failed", "error": str(e)}), 401
            
            
            from models import User
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({"msg": "User not found"}), 404
            
            if user.role not in allowed_roles:
                return jsonify({"msg": f"Unauthorized. Required roles: {', '.join(allowed_roles)}"}), 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def require_auth():
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
