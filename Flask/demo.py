import json
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager()
login_manager.init_app(app)

# When a user tries to access a protected route without being authenticated, Flask-Login automatically redirects them to the login page
login_manager.login_view = 'login'

demo_db = {
    "anant": {
        "username": "anant",
        "password": "123@Pune",
        "email": "ac@gmail.com",
    },
    "raj": {
        "username": "raj",
        "password": "123@Kharadi",
        "email": "raj@gmail.com",
    }
}
# It will store logged in user's data
class User:
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.username
    
    def to_json(self):        
        return {"username": self.username}

prompt_value = "You're an esteemed college professor tasked with crafting {type} questions based on the {content} provided."

class Prompt:
    def __init__(self, type, content):
        self.type = type
        self.content = content

# it will be called after login, when we call other requests
@login_manager.user_loader
def load_user(username):
    if username in demo_db:
        return User(username)
    return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    user_data = demo_db.get(username)
    if user_data and user_data["password"] == password:
        # creating a new user object
        login_user(User(username))
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"})

@app.route('/set_prompt/', methods=["POST"])
@login_required
def set_prompt():
    data = request.json
    global prompt_value
    prompt_value = f"You're an esteemed college professor tasked with crafting {data['type']} questions based on the {data['content']} provided."
    return jsonify({"message": "Prompt value updated successfully"})

@app.route('/get_prompt/', methods=["GET"])
@login_required
def get_prompt():
    global prompt_value
    return jsonify({"prompt_value": prompt_value})

@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"status": 200,
                "data": current_user.to_json()
                }
    else:
        resp = {"status": 401,
                "data": {"message": "Unauthorized"}
                }
    return jsonify(**resp)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(**{'status': 200,
                      'data': {'message': 'logout success'}})
    
if __name__ == "__main__":
    app.run(debug=True)
