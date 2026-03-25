from flask import Blueprint

auth_bp = Blueprint('auth' , __name__ , url_prefix='')

@auth_bp.route('/')
def hello():
    return "Hello Traveller!"

