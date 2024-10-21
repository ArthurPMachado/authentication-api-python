from flask import Flask
from database import database
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

database.init_app(app)

@app.route("/hello", methods=["GET"])
def hello_world():
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)