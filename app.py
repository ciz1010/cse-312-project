from flask import Flask, request, make_response, send_from_directory
from pymongo import MongoClient
import json
from util.post import Post
from util.get import Get
from util.user_exists import User_Exists

app = Flask(__name__)

mongo_client = MongoClient("mongo")   # "mongo", 27017)
db = mongo_client["pROJECTbRANIAC"]
chat_collection = db["chat"]
user_collection = db["user"]
# image_collection = db["images"]
counter = db["count"]
counter.insert_one({"identification": 1})
# print("R", request.path)
@app.route('/')
def main_html_file():
    # render_template() sends the file
    # print(render_template('p.html'))
    # checking for user
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
    ##
    # repo = make_response(send_from_directory('static', 'b.html'))
    # repo = make_response(send_from_directory('static', 'b.html'))
    # repo.headers['Content-Type'] = "text/html"
    repo = make_response(f1)
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo


# JS
@app.route('/b.js')
def main_js_file():
    repo = make_response(send_from_directory('static', 'b.js'))
    # repo.headers['Content-Type'] = "text/javascript"
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo


# CSS
@app.route('/b.css')
def main_css_file():
    repo = make_response(send_from_directory('static', 'b.css'))
    # repo.headers['Content-Type'] = "text/css"
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo


# IMG
@app.route('/static/image/kitten.jpg')
def main_jpg_file():
    repo = make_response(send_from_directory('static', 'image/kitten.jpg'))
    # repo.headers['Content-Type'] = "image/jpeg"
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo

@app.route('/static/image/braniac.png')
def main_png_file():
    repo = make_response(send_from_directory('static', 'image/braniac.png'))
    # repo.headers['Content-Type'] = "image/jpeg"
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo

@app.route('/static/image/favicon.ico')
def main_ico_file():
    repo = make_response(send_from_directory('static', 'image/favicon.ico'))
    # repo.headers['Content-Type'] = "image/jpeg"
    repo.headers['X-Content-Type-Options'] = "nosniff"
    return repo

@app.route('/chat-messages', methods=['GET'])
def chat_messages0():
    response = Get('/chat-messages', chat_collection, user_collection).response

    return response

@app.route('/register', methods=['POST'])
def register():
    #print("Register request body:", request.form)
    # Handle registration logic here
    request_data = json.loads(request.data.decode())
    post_response = Post("/register", request_data, user_collection, request, chat_collection, counter)
    # test = request.data.decode()
    # test = json.loads(request.data.decode())
    return post_response.response    #'Registration successfu' # str(type(test[0]))#'Registration successfu'

@app.route('/login', methods=['POST'])
def login():
    # print("Login request body:", request.form)
    # Handle login logic here
    request_data = json.loads(request.data.decode())
    post_response = Post("/login", request_data, user_collection, request, chat_collection, counter)
    if type(post_response.response) is dict:
        auth_token = post_response.response.get('Auth-Token', "No Auth")
        if auth_token != "No Auth":
            response = make_response("Login Successfu. Auth Token Set")
            response.set_cookie('Auth-Token', auth_token, max_age=3600, httponly=True)
            return response
    return post_response.response

@app.route('/logout', methods=['POST'])
def logout():
    # print("Logout request body:", request.form)
    # Handle logout logic here
    # request_data = json.loads(request.data.decode())
    request_data = None
    post_response = Post("/logout", request_data, user_collection, request, chat_collection, counter)
    if post_response.response == "Auth Token REMOVED from DATABASE":
        response = make_response("Token removed from COOKIES successfully")
        # Set the expiration time of the cookie to a past time
        response.set_cookie('Auth-Token', '', expires=0)
        return response
    return post_response.response


@app.route('/chat-messages', methods=['POST'])
def chat_messages():
    # Get the message text from the request
    # message = request.form.get('message')
    request_data = ""
    post_response = Post("/chat-messages", request_data, user_collection, request, chat_collection, counter).response
    # Check if an image file was uploaded
    # if 'image' in request.files:
    #     image_file = request.files['image']
    #     # Save the image file to a location or process it as needed
    #     # Create the 'uploaded_images' directory if it doesn't exist
    #     if not os.path.exists('uploaded_images'):
    #         os.makedirs('uploaded_images')
    #     # For example, you can save it to disk
    #     image_file.save('uploaded_images/' + image_file.filename)
    #     # Construct a response JSON with message and image URL
    #     response = {'message': message, 'image_url': f'/uploaded_images/{image_file.filename}'}
    # else:
    #     # Construct a response JSON with only the message
    #     response = {'message': message}

    return post_response
    # Return the response as JSON
    # return jsonify(response)


# 'uploaded_images/elephant-small.jpg'


@app.route('/downvote/<int:vote_id>', methods=['POST'])
def down_vote(vote_id):
    request_data = ""
    post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
    #return f"Downvote with ID {vote_id}"
    return post_response.response

@app.route('/upvote/<int:vote_id>', methods = ['POST'])
def up_vote(vote_id):
    request_data = ""
    post_response = Post(request.url, request_data, user_collection, request, chat_collection, counter)
    return post_response.response
    # return f"Upvote with ID {vote_id}"

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
