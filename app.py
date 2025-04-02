#
#
# from flask import Flask, render_template, request, jsonify
# import subprocess
# import os
# import google.generativeai as gen_ai
# from flask_cors import CORS
# from pymongo import MongoClient
# import bcrypt
# # Replace with your actual Google API key
# GOOGLE_API_KEY = "AIzaSyCxO4iKszCQ9KPFGCbY5Xzj7SBOaM2tHk0"
#
#
# # Configure the Gemini API
# gen_ai.configure(api_key=GOOGLE_API_KEY)
# model = gen_ai.GenerativeModel("gemini-pro")
# app = Flask(__name__)
# CORS(app)
#
# # MongoDB configuration
# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if needed
# db = client['signupDB']
# users_collection = db['users']
# # Dictionary to keep track of processes
# processes = {}
#
# # Route to display tools page
# @app.route('/tools')
# def tools():
#     return render_template('tools.html')
# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/chatbot')
# def chatbot():
#     return render_template('chatbot.html')
# @app.route('/login', methods=['GET'])
# def login():
#     return render_template('login.html')
# @app.route('/login', methods=['POST'])
# def login_user():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')
#
#     # Retrieve user from database
#     user = users_collection.find_one({'email': email})
#
#     if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
#         # Create a token or session if needed
#         token = "example-token"  # Replace with real token generation logic
#         return jsonify({'message': 'Login successful', 'token': token}), 200
#     else:
#         return jsonify({'message': 'Invalid email or password'}), 401
#
# @app.route('/signup', methods=['GET'])
# def render_signup():
#     return render_template('signup.html')
# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#
#     # Check if username already exists
#     if users_collection.find_one({'username': username}):
#         return jsonify({'field': 'username', 'message': 'Username already taken'}), 400
#
#     # Check if email already exists
#     if users_collection.find_one({'email': email}):
#         return jsonify({'field': 'email', 'message': 'Email already registered'}), 400
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     # Insert the new user
#     new_user = {
#         'username': username,
#         'email': email,
#         'password': hashed_password,  # In a real application, hash the password
#     }
#     users_collection.insert_one(new_user)
#
#     return jsonify({'message': 'User registered successfully'}), 201
#
# # Route to start a Python script
# @app.route('/start', methods=['POST'])
# def start_script():
#     tool_name = request.json.get('tool_name')
#     script_path = os.path.join('scripts', f'{tool_name}.py')
#
#     if tool_name in processes:
#         return jsonify({'message': 'Script is already running!'}), 400
#
#     if os.path.exists(script_path):
#         process = subprocess.Popen(['python', script_path])
#         processes[tool_name] = process
#         return jsonify({'message': 'Script started successfully!'}), 200
#     else:
#         return jsonify({'message': 'Script not found!'}), 404
#
# # Route to stop a Python script
# @app.route('/stop', methods=['POST'])
# def stop_script():
#     tool_name = request.json.get('tool_name')
#
#     if tool_name in processes:
#         process = processes[tool_name]
#         process.terminate()
#         process.wait()
#         del processes[tool_name]
#         return jsonify({'message': 'Script stopped successfully!'}), 200
#     else:
#         return jsonify({'message': 'Script is not running!'}), 400
# @app.route("/get-bot-response", methods=["POST"])
# def get_bot_response():
#     data = request.get_json()
#
#     # Extract user message and session ID
#     user_message = data.get("message", "").strip()
#     session_id = data.get("session_id", "default-session")
#
#     if not user_message:
#         return jsonify({"response": "Please provide a valid message."}), 400
#
#     try:
#         # Start or continue a chat session
#         chat_session = model.start_chat(history=[])
#         response = chat_session.send_message(user_message)
#
#         # Return the bot's response
#         return jsonify({"response": response.text})
#     except Exception as e:
#         return jsonify({"response": f"Error: {str(e)}"}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#





# from flask import Flask, render_template, request, jsonify
# import subprocess
# import os
# import google.generativeai as gen_ai
# from flask_cors import CORS
# from pymongo import MongoClient
# import bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# import jwt
#
# # Replace with your actual Google API key
# GOOGLE_API_KEY = "AIzaSyCxO4iKszCQ9KPFGCbY5Xzj7SBOaM2tHk0"
#
# # Configure the Gemini API
# gen_ai.configure(api_key=GOOGLE_API_KEY)
# model = gen_ai.GenerativeModel("gemini-pro")
# app = Flask(__name__)
# CORS(app)
#
# # MongoDB configuration
# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if needed
# db = client['signupDB']
# users_collection = db['users']
#
# # Secret key for JWT
# app.config["JWT_SECRET_KEY"] = os.urandom(32).hex()
# jwt_manager = JWTManager(app)
#
# # Dictionary to keep track of processes
# processes = {}
#
#
# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/forgot-password')
# def forgot_password():
#     return render_template('forgot_password.html')
#
# @app.route('/tools')
# def tools():
#     return render_template('tools.html')
#
#
# @app.route('/chatbot')
#
# def chatbot():
#     return render_template('chatbot.html')
# @app.route('/login', methods=['GET'])
# def login():
#     return render_template('login.html')
#
# @app.route('/login', methods=['POST'])
# def login_user():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')
#
#     user = users_collection.find_one({'email': email})
#
#     if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
#         access_token = create_access_token(identity=email)
#         return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
#     else:
#         return jsonify({'message': 'Invalid email or password'}), 401
#
# @app.route('/signup', methods=['GET'])
# def render_signup():
#     return render_template('signup.html')
# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#
#     if users_collection.find_one({'username': username}):
#         return jsonify({'field': 'username', 'message': 'Username already taken'}), 400
#
#     if users_collection.find_one({'email': email}):
#         return jsonify({'field': 'email', 'message': 'Email already registered'}), 400
#
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     new_user = {
#         'username': username,
#         'email': email,
#         'password': hashed_password,
#     }
#     users_collection.insert_one(new_user)
#
#     return jsonify({'message': 'User registered successfully'}), 201
#
#
# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
#
#
# @app.route('/start', methods=['POST'])
# @jwt_required()
# def start_script():
#     tool_name = request.json.get('tool_name')
#     script_path = os.path.join('scripts', f'{tool_name}.py')
#
#     if tool_name in processes:
#         return jsonify({'message': 'Script is already running!'}), 400
#
#     if os.path.exists(script_path):
#         process = subprocess.Popen(['python', script_path])
#         processes[tool_name] = process
#         return jsonify({'message': 'Script started successfully!'}), 200
#     else:
#         return jsonify({'message': 'Script not found!'}), 404
#
#
# @app.route('/stop', methods=['POST'])
# @jwt_required()
# def stop_script():
#     tool_name = request.json.get('tool_name')
#
#     if tool_name in processes:
#         process = processes[tool_name]
#         process.terminate()
#         process.wait()
#         del processes[tool_name]
#         return jsonify({'message': 'Script stopped successfully!'}), 200
#     else:
#         return jsonify({'message': 'Script is not running!'}), 400
#
#
# @app.route("/get-bot-response", methods=["POST"])
# @jwt_required()
# def get_bot_response():
#     data = request.get_json()
#     user_message = data.get("message", "").strip()
#
#     if not user_message:
#         return jsonify({"response": "Please provide a valid message."}), 400
#
#     try:
#         chat_session = model.start_chat(history=[])
#         response = chat_session.send_message(user_message)
#         return jsonify({"response": response.text})
#     except Exception as e:
#         return jsonify({"response": f"Error: {str(e)}"}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, jsonify
import subprocess
import os
import google.generativeai as gen_ai
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Replace with your actual Google API key
GOOGLE_API_KEY = "AIzaSyCxO4iKszCQ9KPFGCbY5Xzj7SBOaM2tHk0"

# Configure the Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.0-flash")
app = Flask(__name__)
CORS(app)

# MongoDB configuration
client = MongoClient('mongodb+srv://project_k:R5lbJOQQ953HPHv1@cluster1.gi5pjk9.mongodb.net/?retryWrites=true&w=majority')  # Replace with your MongoDB URI if needed
db = client['signupDB']
users_collection = db['users']

# Secret key for JWT
app.config["JWT_SECRET_KEY"] = os.urandom(32).hex()
jwt_manager = JWTManager(app)

# Dictionary to keep track of processes
processes = {}
# Store OTPs temporarily (Ideally, use Redis for better scalability)
otp_store = {}

# Function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via email
def send_otp_email(email, otp):
    sender_email = "madanala02@gmail.com"
    sender_password = "dnau uque grgk jzpz"
    subject = "Your OTP for Password Reset"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    body = f"Your OTP for resetting your password is: {otp}\nThis OTP is valid for 30 seconds."
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

# Route to handle forgot password request
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not users_collection.find_one({'email': email}):
        return jsonify({"message": "Email doesn't exist!"}), 500
    if email in otp_store and time.time() - otp_store[email]["timestamp"] > 30:  # Expire OTP after 30 seconds
        del otp_store[email]
    if email in otp_store:
        return jsonify({"message": "Email already sent!"}), 500
    # Generate OTP and store it temporarily
    otp = generate_otp()
    otp_store[email] = {"otp": otp, "timestamp": time.time()}   # Store OTP (consider using Redis for expiry feature)

    # Send OTP to email
    if send_otp_email(email, otp):
        return jsonify({"message": "OTP sent successfully", "email": email}), 200
    else:
        return jsonify({"message": "Failed to send OTP"}), 500
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get("email")
    entered_otp = data.get("otp")

    if not email or not entered_otp:
        return jsonify({"message": "Email and OTP are required"}), 400

    if email not in otp_store:
        return jsonify({"message": "OTP expired or not requested"}), 400
    print(otp_store)
    stored_otp_info = otp_store[email]
    stored_otp = stored_otp_info["otp"]
    timestamp = stored_otp_info["timestamp"]

    if time.time() - timestamp > 30:  # Expire OTP after 30 seconds
        del otp_store[email]
        return jsonify({"message": "OTP expired"}), 400

    if entered_otp == stored_otp:
        del otp_store[email]  # Remove OTP after verification
        return jsonify({"message": "OTP verified successfully"}), 200
    else:
        return jsonify({"message": "Invalid OTP"}), 400

# Route to reset password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("password")

    if not email or not new_password:
        return jsonify({"message": "Email and new password are required"}), 400
    if len(new_password)< 8:
        return jsonify({"message": "Password need to be atleast 8 characters"}), 400
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    result = users_collection.update_one(
        {"email": email},  # Find user by email
        {"$set": {"password": hashed_password}}  # Update password
    )

     # Save new password (store securely in real app)
    return jsonify({"message": "Password reset successfully"}), 200


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/forgot-password',methods=['GET'])
def render_forgot_password():
    return render_template('forgot_password.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')


@app.route('/chatbot')

def chatbot():
    return render_template('chatbot.html')
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity=email)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/signup', methods=['GET'])
def render_signup():
    return render_template('signup.html')
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if users_collection.find_one({'username': username}):
        return jsonify({'field': 'username', 'message': 'Username already taken'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'field': 'email', 'message': 'Email already registered'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password,
    }
    users_collection.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/start', methods=['POST'])
def start_script():
    tool_name = request.json.get('tool_name')
    script_path = os.path.join('scripts', f'{tool_name}.py')

    if tool_name in processes:
        return jsonify({'message': 'Script is already running!'}), 400

    if os.path.exists(script_path):
        process = subprocess.Popen(['python', script_path])
        processes[tool_name] = process
        return jsonify({'message': 'Script started successfully!'}), 200
    else:
        return jsonify({'message': 'Script not found!'}), 404


@app.route('/stop', methods=['POST'])
def stop_script():
    tool_name = request.json.get('tool_name')

    if tool_name in processes:
        process = processes[tool_name]
        process.terminate()
        process.wait()
        del processes[tool_name]
        return jsonify({'message': 'Script stopped successfully!'}), 200
    else:
        return jsonify({'message': 'Script is not running!'}), 400


@app.route("/get-bot-response", methods=["POST"])
def get_bot_response():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please provide a valid message."}), 400

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
