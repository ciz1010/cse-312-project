import bcrypt
import secrets
import hashlib
from util.user_exists import User_Exists


def stop_html_injection(w):
    u = w.replace("&", "&amp")
    u = u.replace("<", "&lt")
    u = u.replace(">", "&gt")
    return u


def register(request_data_list, user_collection):
    username = request_data_list[0]
    password = request_data_list[1]
    password2 = request_data_list[2]

    if password == password2:
        username = stop_html_injection(username)
        password = stop_html_injection(password)

        # username availability
        is_username_available = user_collection.find_one({"username": username})

        if is_username_available is None:
            # salt & hash
            print("Good Password")
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode(), salt)

            # set xsrf
            xsrf_token = secrets.token_urlsafe(30)

            user_collection.insert_one({'username': username, 'password': password, "xsrf_token": xsrf_token})
            print("I have registered")
            response = "Registration SuccessfuL"
        else:
            response = "Username tAKEN"
    else:
        response = "Passwords do not MMATCH!!!"

    return response


def login(request_data_list, user_collection):
    username = request_data_list[0]
    password = request_data_list[1]

    username = stop_html_injection(username)
    password = stop_html_injection(password)

    datat = user_collection.find_one({"username": username}, {"_id": 0})
    if datat is not None:
        print("Found")
        datati = datat['password']
        right_pass = bcrypt.checkpw(password.encode(), datati)
        if right_pass is True:
            print("datat['xsrf_token']: ", datat["xsrf_token"])
            auth_token = secrets.token_urlsafe(20)

            hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
            user_collection.update_one({'username': username}, {"$set": {'Auth-Token': hashed_auth_token}})
            response = {'Auth-Token': auth_token}
        else:
            response = "Incorrect Password"
    else:

        response = "Username not fOUND"

    return response


#
#
def logout(request, user_collection):
    print("Cookies: ", request.cookies)
    Auth = request.cookies.get('Auth-Token')
    print("Auth: ", Auth)

    if Auth:
        hashed_auth_token = hashlib.sha256(Auth.encode()).hexdigest()
        print("hashed_auth: ", hashed_auth_token)
        user_log = user_collection.find_one({"Auth-Token": hashed_auth_token})
        print("I am not guest")
        # Remove the Auth_Token field from the document
        print("user_log: ", user_log)
        if user_log:
            print("user_log: ", user_log)
            user_collection.update_one({"Auth-Token": hashed_auth_token}, {"$unset": {"Auth-Token": ""}})
            response = "Auth Token REMOVED from DATABASE"
            # user_log.update_one({})
        else:
            response = "Auth Token does not belong to any user"
    else:
        response = "No Auth TOKEN found"

    return response


def chat_messages(request, chat_collection, counter, user_collection):
    the_message = request.form.get('message')
    the_message = stop_html_injection(the_message)
    the_image = request.files['image']
    the_image = the_image.read()
    user_exists = User_Exists(request, user_collection).user_exists

    if user_exists is not None:
        print("request.headers.get('X-XSRF-Token'): ", request.headers.get('X-XSRF-Token'))
        print("user_exists['xsrf_token']: ", user_exists['xsrf_token'])
        if request.headers.get('X-XSRF-Token') == user_exists['xsrf_token']:
            message_id = counter.find_one_and_update({}, {"$inc": {"identification": 1}})
            chat_collection.insert_one(
                {"username": user_exists["username"], "message": the_message,
                 'identification': message_id["identification"], "image": the_image, "Upvote": 0, "Downvote": 0,
                 "NameList": []})
            response = "User message saved to database"
        else:
            response = "Bad Token"


    else:
        chat_collection.insert_one(
            {"username": "Guest", "message": the_message, 'identification': 0, "image": the_image})
        print("I inserted into chat_collect")
        response = "Guest message saved to database"

    return response


def upvote(chat_collection, user_collection, request):
    user_exists = User_Exists(request, user_collection).user_exists
    splitonslash = request.path.split('/')
    idd = splitonslash[2]
    chat_exists = chat_collection.find_one({'identification': int(idd)})
    if int(idd) != 0:
        if user_exists is not None:
            if chat_exists is not None:
                username = user_exists["username"]
                if username not in chat_exists["NameList"]:
                    # chat_exists["Upvote"] = int(chat_exists["Upvote"]) + 1
                    # chat_exists["NameList"].append(username)
                    Upvote = int(chat_exists["Upvote"]) + 1
                    NameList = chat_exists["NameList"]
                    NameList.append(username)
                    chat_collection.update_one({'identification': int(idd)}, {"$set": {'Upvote': Upvote}})
                    chat_collection.update_one({'identification': int(idd)}, {"$set": {'NameList': NameList}})

                    return "Upvote recorded"
                else:
                    return "Only one upvote per user"
            else:
                return "chat message does not exist"
        else:
            return "Guest cannot Upvote"
    else:
        return "Guests cannot receive Upvotes"


def downvote(chat_collection, user_collection, request):
    user_exists = User_Exists(request, user_collection).user_exists
    splitonslash = request.path.split('/')
    idd = splitonslash[2]
    chat_exists = chat_collection.find_one({'identification': int(idd)})
    if int(idd) != 0:
        if user_exists is not None:
            if chat_exists is not None:
                username = user_exists["username"]
                if username not in chat_exists["NameList"]:
                    # chat_exists["Downvote"] = int(chat_exists["Downvote"]) + 1
                    # chat_exists["NameList"].append(username)
                    Downvote = int(chat_exists["Downvote"]) + 1
                    NameList = chat_exists["NameList"]
                    NameList.append(username)
                    chat_collection.update_one({'identification': int(idd)}, {"$set": {'Downvote': Downvote}})
                    chat_collection.update_one({'identification': int(idd)}, {"$set": {'NameList': NameList}})
                    return "Downvote recorded"
                else:
                    return "not allowed to downvote twice"
            else:
                return "chat message does not exist 2"
        else:
            return "Guest cannot Downvote"

    else:
        return "Guests cannot receive Downvotes"


class Post:
    def __init__(self, request_path, request_data_list, user_collection, request, chat_collection, counter):
        self.response = ""

        if request_path == '/register':
            self.response = register(request_data_list, user_collection)

        elif request_path == '/login':
            self.response = login(request_data_list, user_collection)

        elif request_path == '/logout':
            self.response = logout(request, user_collection)

        elif request_path == '/chat-messages':
            self.response = chat_messages(request, chat_collection, counter, user_collection)

        elif '/upvote' in request_path:
            self.response = upvote(chat_collection, user_collection, request)

        elif '/downvote' in request_path:
            self.response = downvote(chat_collection, user_collection, request)
