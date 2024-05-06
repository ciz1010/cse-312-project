# from flask import Flask, request, make_response, send_from_directory
# from pymongo import MongoClient
# import json
# from util.post import Post
# from util.get import Get
# from util.user_exists import User_Exists
#
# app = Flask(__name__)
#
# mongo_client = MongoClient("mongo")  # "mongo", 27017)
# db = mongo_client["pROJECTbRANIAC"]
# chat_collection = db["chat"]
# user_collection = db["user"]
# # image_collection = db["images"]
# counter = db["count"]
# counter.insert_one({"identification": 1})
#
#
# # print("R", request.path)
# @app.route('/')
# def main_html_file():
#     # render_template() sends the file
#     # print(render_template('p.html'))
#     # checking for user
#     f = open('static/b.html', encoding='utf-8')
#     f1 = f.read()
#     user_exists = User_Exists(request, user_collection).user_exists
#     if user_exists is not None:
#         xsrf_token = user_exists['xsrf_token']
#         username = user_exists['username']
#         f1 = f1.replace('{{xsrfToken}}', str(xsrf_token))
#         f1 = f1.replace('{{Guest}}', str(username))
#     else:
#         f1 = f1.replace('{{Guest}}', "Guest")
#     ##
#     # repo = make_response(send_from_directory('static', 'b.html'))
#     # repo = make_response(send_from_directory('static', 'b.html'))
#     # repo.headers['Content-Type'] = "text/html"
#     repo = make_response(f1)
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# # JS
# @app.route('/b.js')
# def main_js_file():
#     repo = make_response(send_from_directory('static', 'b.js'))
#     # repo.headers['Content-Type'] = "text/javascript"
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# # CSS
# @app.route('/b.css')
# def main_css_file():
#     repo = make_response(send_from_directory('static', 'b.css'))
#     # repo.headers['Content-Type'] = "text/css"
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# # IMG
# @app.route('/static/image/braniac.jpg')
# def main_jpg_file():
#     repo = make_response(send_from_directory('static', 'image/braniac.jpg'))
#     # repo.headers['Content-Type'] = "image/jpeg"
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# @app.route('/static/image/braniac.png')
# def main_png_file():
#     repo = make_response(send_from_directory('static', 'image/braniac.png'))
#     # repo.headers['Content-Type'] = "image/jpeg"
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# @app.route('/static/image/favicon.ico')
# def main_ico_file():
#     repo = make_response(send_from_directory('static', 'image/favicon.ico'))
#     # repo.headers['Content-Type'] = "image/jpeg"
#     repo.headers['X-Content-Type-Options'] = "nosniff"
#     return repo
#
#
# @app.route('/chat-messages', methods=['GET'])
# def chat_messages0():
#     response = Get('/chat-messages', chat_collection, user_collection).response
#     # response.headers['X-Content-Type-Options'] = 'nosniff'
#     return response
#
#
# @app.route('/register', methods=['POST'])
# def register():
#     # print("Register request body:", request.form)
#     # Handle registration logic here
#     request_data = json.loads(request.data.decode())
#     post_response = Post("/register", request_data, user_collection, request, chat_collection, counter).response
#     # post_response.headers['X-Content-Type-Options'] = 'nosniff'
#     # test = request.data.decode()
#     # test = json.loads(request.data.decode())
#     return post_response  # 'Registration successfu' # str(type(test[0]))#'Registration successfu'
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     # print("Login request body:", request.form)
#     # Handle login logic here
#     request_data = json.loads(request.data.decode())
#     post_response = Post("/login", request_data, user_collection, request, chat_collection, counter)
#     if type(post_response.response) is dict:
#         auth_token = post_response.response.get('Auth-Token', "No Auth")
#         if auth_token != "No Auth":
#             response = make_response("Login Successfu. Auth Token Set")
#             response.set_cookie('Auth-Token', auth_token, max_age=3600, httponly=True)
#             return response
#     # post_response.headers['X-Content-Type-Options'] = 'nosniff'
#     return post_response
#
#
# @app.route('/logout', methods=['POST'])
# def logout():
#     # print("Logout request body:", request.form)
#     # Handle logout logic here
#     # request_data = json.loads(request.data.decode())
#     request_data = None
#     post_response = Post("/logout", request_data, user_collection, request, chat_collection, counter)
#     if post_response.response == "Auth Token REMOVED from DATABASE":
#         response = make_response("Token removed from COOKIES successfully")
#         # Set the expiration time of the cookie to a past time
#         response.set_cookie('Auth-Token', '', expires=0, httponly=True)
#         return response
#     return post_response.response
#
#
# @app.route('/chat-messages', methods=['POST'])
# def chat_messages():
#     # Get the message text from the request
#     # message = request.form.get('message')
#     request_data = ""
#     post_response = Post("/chat-messages", request_data, user_collection, request, chat_collection, counter).response
#
#     return post_response
#     # Return the response as JSON
#     # return jsonify(response)
#
#
# # 'uploaded_images/elephant-small.jpg'
#
#
# @app.route('/downvote/<int:vote_id>', methods=['POST'])
# def down_vote():
#     request_data = ""
#     post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
#     # return f"Downvote with ID {vote_id}"
#     return post_response.response
#
#
# @app.route('/upvote/<int:vote_id>', methods=['POST'])
# def up_vote():
#     request_data = ""
#     post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
#     return post_response.response
#     # return f"Upvote with ID {vote_id}"
#
#
# if __name__ == '__main__':
#     app.run(debug=True, port=8080, host='0.0.0.0')
################################################################################################################@######3
# was able to trim code inn a couple of hours. Still a little attached to my previous implementation though ^

from flask import Flask, make_response, send_from_directory, request, Response
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
from collections import defaultdict
import time
from util.post import Post
from util.get import Get
from util.user_exists import User_Exists

app = Flask(__name__)
socketio = SocketIO(app)

mongo_client = MongoClient("mongo")  # "mongo", 27017)
db = mongo_client["pROJECTbRANIAC"]
chat_collection = db["chat"]
user_collection = db["user"]
counter = db["count"]
counter.insert_one({"identification": 1})
IPS = defaultdict(lambda: {'requestTimestamps': [], 'timeBlocked': 0}) # dict that stores the amount of requests and the timestamps for each request for each ip_address address
MAX_REQUESTS = 50
REQUEST_WINDOW = 10
TIMEOUT = 30

def get_mimetype(file_extension):
    mime_types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'text/javascript',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.ico': 'image/x-icon',
        # Add more file extensions and MIME types as needed
    }
    return mime_types.get(file_extension.lower(), 'application/octet-stream')

# Define a function to set the X-Content-Type-Options header for all responses
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Function to check if an IP address is blocked
def checkIPBlocked(ip_address):
    current_time = time.time()
    return IPS[ip_address]['timeBlocked'] > current_time

@app.before_request
def limit_ip():
    ip_address = request.headers["X-Real-IP"]
    
    if checkIPBlocked(ip_address):
        return serve_error()
    
    ip_info = IPS[ip_address]
    # this removes all the timestamps that are not within the window
    ip_info['requestTimestamps'] = [timE for timE in ip_info['requestTimestamps'] if time.time() - timE <= REQUEST_WINDOW] 

    num_of_requests_in_window = len(ip_info['requestTimestamps'])
    
    if num_of_requests_in_window > MAX_REQUESTS:
        ip_info['timeBlocked'] = time.time() + TIMEOUT
        return serve_error()
    
    ip_info['requestTimestamps'].append(time.time()) 

def serve_error():
    f = open('nginx/error.html', encoding='utf-8')
    f1 = f.read()
    response = make_response(f1, 429)
    return response
# Define a function to set the X-Content-Type-Options header for all responses
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def serve_homepage():
    # Load and return the homepage HTML file
    f = open('static/b.html', encoding='utf-8')
    f1 = f.read()
    user_exists = User_Exists(request, user_collection).user_exists
    if user_exists is not None:
        xsrf_token = user_exists['xsrf_token']
        username = user_exists['username']
        f1 = f1.replace('{{xsrfToken}}', str(xsrf_token))
        f1 = f1.replace('{{Guest}}', str(username))
    else:
        f1 = f1.replace('{{Guest}}', "Guest")

    # Create response with headers
    response = Response(f1, mimetype='text/html')
    response.headers['X-Content-Type-Options'] = 'nosniff'

    return response

# Route to serve static files
@app.route('/<path:filename>')
def serve_static_file(filename):
    directory = 'static'
    # file_path = directory + '/' + filename
    mimetype = get_mimetype('.' + filename.split('.')[-1])  # Extract file extension
    return send_from_directory(directory, filename, mimetype=mimetype)

# Want to handle the websocket connection

@socketio.on('connect')
def connected():
    print('Client connected')
    #let em know you connecting


# Want to handle the websocket disconnect
@socketio.on('disconnect')
def disconnected():
    print('Client disconnected')
    #let em know you disconnecting


#When client sends a message
@socketio.on('message')
def messagecoming(data):
    socketio.emit('clientsent', {'message': 'Got your message!'})
#tells client the message is got
# Route to get chat messages
@app.route('/chat-messages', methods=['GET'])
def get_chat_messages():
    response = Get('/chat-messages', chat_collection, user_collection).response
    return response

# Route to handle registration
@app.route('/register', methods=['POST'])
def register():
    request_data = json.loads(request.data.decode())
    post_response = Post("/register", request_data, user_collection, request, chat_collection, counter).response
    return post_response

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    request_data = json.loads(request.data.decode())
    post_response = Post("/login", request_data, user_collection, request, chat_collection, counter)
    if type(post_response.response) is dict:
        auth_token = post_response.response.get('Auth-Token', "No Auth")
        if auth_token != "No Auth":
            response = make_response("Login Successfu. Auth Token Set")
            response.set_cookie('Auth-Token', auth_token, max_age=3600, httponly=True)
            return response
    return post_response.response

# Route to handle logout
@app.route('/logout', methods=['POST'])
def logout():
    request_data = None
    post_response = Post("/logout", request_data, user_collection, request, chat_collection, counter)
    if post_response.response == "Auth Token REMOVED from DATABASE":
        response = make_response("Token removed from COOKIES successfully")
        response.set_cookie('Auth-Token', '', expires=0, httponly=True)
        return response
    return post_response.response

# Route to handle creating chat messages
@app.route('/chat-messages', methods=['POST'])
def create_chat_message():
    request_data = ""
    post_response = Post("/chat-messages", request_data, user_collection, request, chat_collection, counter).response
    return post_response

# Route to handle downvoting
@app.route('/downvote/<int:vote_id>', methods=['POST'])
def down_vote(vote_id):
    request_data = ""
    post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
    return post_response.response

# Route to handle upvoting
@app.route('/upvote/<int:vote_id>', methods=['POST'])
def up_vote(vote_id):
    request_data = ""
    post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
    return post_response.response

if __name__ == '__main__':
    #app.run(debug=True, port=8080, host='0.0.0.0')
    socketio.run(app, debug=True, port=8080, host='0.0.0.0',  allow_unsafe_werkzeug=True)






