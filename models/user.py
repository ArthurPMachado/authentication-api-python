from app import database

class User(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  username = database.Column(database.String(80), nullable=False, unique=True)
  password = database.Column(database.String(80), nullable=False)