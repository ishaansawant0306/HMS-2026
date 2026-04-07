from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail

# Shared Flask extensions instance holders
# These are initialized once in app.create_app()

db = SQLAlchemy()
cache = Cache()
mail = Mail()
