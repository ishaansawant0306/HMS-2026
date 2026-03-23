from app import app, db
from models import User
print('OK', app.name, db.__class__.__name__, User.__name__)
