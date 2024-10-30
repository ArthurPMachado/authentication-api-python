from database import database
from flask_login import UserMixin

class User(database.Model, UserMixin):
  id = database.Column(database.Integer, primary_key=True)
  username = database.Column(database.String(80), nullable=False, unique=True)
  password = database.Column(database.String(80), nullable=False)
  role = database.Column(database.String(80), nullable=False, default='user')