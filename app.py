import bcrypt
from flask import Flask, jsonify, request
from database import database
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-authentication'

login_manager = LoginManager()

database.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
      login_user(user)
      print(current_user.is_authenticated)

      response = jsonify({
        "message": "Login successful"
      })
      return response
  
  response = jsonify({
    'message': 'Invalid Credentials'
  }), 400

  return response

@app.route('/logout', methods=["GET"])
@login_required
def logout():
  logout_user()
  response = jsonify({
    "message": "Logout successful"
  })

  return response

@app.route('/user', methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

    user = User(username=username, password=hashed_password, role='user')

    database.session.add(user)
    database.session.commit()

    response = jsonify({
      "message": "User created successfully"
    })

    return response

  response = jsonify({
    "message": "Invalid data"
  }), 400

  return response

@app.route('/user/<int:id>', methods=["GET"])
@login_required
def get_user(id):
  user = User.query.get(id)

  if user:
    return {
      "username": user.username
    }
  
  response = jsonify({
    "message": "User not found"
  }), 404

  return response

@app.route('/user/<int:id>', methods=["PUT"])
@login_required
def update_user(id):
  data = request.json
  user = User.query.get(id)

  if id != current_user.id and current_user.role == 'user':
    response = jsonify({
      "message": "Operation not allowed"
    }), 403

    return response

  if user and data.get("password"):
    user.password = data.get("password")

    database.session.commit()

    response = jsonify({
      "message": f"User {id} updated successfully"
    })

    return response 
  
  response = jsonify({
    "message": "User not found"
  }), 404

  return response

@app.route('/user/<int:id>', methods=["DELETE"])
@login_required
def delete_user(id):
  user = User.query.get(id)

  if current_user.role != 'admin':
    response = jsonify({
      "message": "Operation not allowed"
    }), 403

    return response

  if id == current_user.id:
    response = jsonify({
      "message": f"Deletion of user {id} not allowed"
    }), 403

    return response

  if user:
    database.session.delete(user)
    database.session.commit()

    response = jsonify({
      "message": f"User {id} deleted successfully"
    })

    return response
  
  response = jsonify({
    "message": "User not found"
  }), 404

  return response

if __name__ == "__main__":
  app.run(debug=True)