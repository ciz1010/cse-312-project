import json
import bcrypt
import secrets
import hashlib

# import util.auth
# from util.errors import Errors
from util.user_exists import User_Exists


def stop_html_injection(w):
    u = w.replace("&", "&amp")
    u = u.replace("<", "&lt")
    u = u.replace(">", "&gt")
    return u


def split_body_register_and_login(body):
    body = body.decode()
    split_on_ampersand = body.split('&')
    username = split_on_ampersand[0].split('=')
    username = username[1]
    password = split_on_ampersand[1].split('=')
    password = password[1]
    return username, password


def register(request_data_list, user_collection):
    # usernameANDpassword = util.auth.extract_credentials(request.body)
    username = request_data_list[0]
    password = request_data_list[1]
    print("UPUPUPUPUP: ", username, password)
    # username, password = split_body_register_and_login(request.body)
    # username, password = split_body_register_and_login(request.body)
    # username, password = split_body_register_and_login(request.body)
    # print("username: ", username)
    username = stop_html_injection(username)
    # username = util.auth.extract_credentials(username)
    # print("username: ", username)
    password = stop_html_injection(password)
    # password = util.auth.extract_credentials(password)

    # checks if password follows defined conventions
    # if util.auth.validate_password(password) is False:
    #     print("Bad Password")
    #     # disp = "Password should have at least:\n 8 characters\n 1 number\n 1 lower case letter\n 1 upper case letter\n 1of these special characters: {'!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '='}\nNo other characters must be used except the ones stated above."
    #     # return Errors("404", disp, request).error
    #     response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\n\r\n"
    #     return response

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
        # response = f"HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nYou are now a registered user!!!"
        # response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\n\r\n"
        response = "Registration SuccessfuL"
    else:
        response = "Username tAKEN"

    return response


def login(request_data_list, user_collection):
    username = request_data_list[0]
    password = request_data_list[1]
    # usernameANDpassword = util.auth.extract_credentials(request.body)
    # username = usernameANDpassword[0]
    # password = usernameANDpassword[1]
    print("UPUPUPUPUP2: ", username, password)
    # username, password = split_body_register_and_login(request.body)
    # print("username: ", username)
    username = stop_html_injection(username)
    # username = util.auth.extract_credentials(username)
    # print("username: ", username)
    password = stop_html_injection(password)
    # password = util.auth.extract_credentials(password)
    # check if username exists
    # {"_id": 0} drops id so code doesn't error
    response = ""
    datat = user_collection.find_one({"username": username}, {"_id": 0})
    if datat is not None:
        print("Found")
        datati = datat['password']
        right_pass = bcrypt.checkpw(password.encode(), datati)
        if right_pass is True:
            # set xsrf token
            # xsrf_token = secrets.token_urlsafe(30)

            # xsrf_token = datat["xsrf_token"]
            # f = open('public/index.html', encoding='utf-8')
            # f1 = f.read()
            # f1 = f1.replace('{{xsrfToken}}', str(xsrf_token))
            # f.close()
            print("datat['xsrf_token']: ", datat["xsrf_token"])
            auth_token = secrets.token_urlsafe(20)
            # response = f"HTTP/1.1 200 OK\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain; charset=utf-8\r\nSet-Cookie: Auth-Token={auth_token}; Max-Age=3600; HttpOnly\r\n\r\nYou have been logged in!!!"
            # response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nSet-Cookie: Auth-Token={auth_token}; Max-Age=3600; HttpOnly\r\nLocation: /\r\n\r\n"     # Content-Length: {len(f1.encode())}\r\nLocation: /\r\n\r\n{f1}"
            #
            hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
            # user_databasee0.insert_one({"Auth-Token": hashed_auth_token})
            user_collection.update_one({'username': username}, {"$set": {'Auth-Token': hashed_auth_token}})
            response = {'Auth-Token': auth_token}
        else:
            print("Bad pASSWORD 2")
            # disp = "Username does not exist, or password does not match1"
            # response = Errors("404", disp, request).error
            # response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\n\r\n"     # Content-Length: {len(f1.encode())}\r\nLocation: /\r\n\r\n{f1}"
            response = "Incorrect Password"
    else:
        print("Not Found")
        # disp = "Username does not exist, or password does not match2"
        # response = Errors("404", disp, request).error
        # response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\n\r\n"  # Content-Length: {len(f1.encode())}\r\nLocation: /\r\n\r\n{f1}"
        response = "Username not fOUND"

    return response


#
#
def logout(request, user_collection):
    # response = f"HTTP/1.1 302 REDIRECT\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8\r\nSet-Cookie: Auth-Token=None; Max-Age=3600; HttpOnly\r\nLocation: /\r\n\r\n"

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
    the_image = request.files['image']
    the_image = the_image.read()
    user_exists = User_Exists(request, user_collection).user_exists
    # message_dict = json.loads(request.body)
    # the_message = stop_html_injection(message_dict["message"])
    # print("message dict: ", message_dict, "type(message_dict): ", type(message_dict))
    # print(".val:", message_dict["message"])
    print("user_exists: ", user_exists)
    if user_exists is not None:
        print("request.headers.get('X-XSRF-Token'): ", request.headers.get('X-XSRF-Token'))
        print("user_exists['xsrf_token']: ", user_exists['xsrf_token'])
        if request.headers.get('X-XSRF-Token') == user_exists['xsrf_token']:
            message_id = counter.find_one_and_update({}, {"$inc": {"identification": 1}})
            chat_collection.insert_one(
                {"username": user_exists["username"], "message": the_message,
                 'identification': message_id["identification"], "image": the_image, "Upvote": 0, "Downvote": 0,
                 "NameList": []})
            # # Updating Code for the AO
            # body = {"username": user_exists["username"], "message": the_message,
            #         'identification': message_id["identification"]}
            # body = json.dumps(body)
            # response = f"HTTP/1.1 201 Created\r\nX-Content-Type-Options: nosniff\r\n\r\n{body}"
            response = "User message saved to database"
        else:
            response = "Bad Token"
            # response = f"HTTP/1.1 403 Forbidden\r\nX-Content-Type-Options: nosniff\r\nContent-Length: {len(disp.encode())}\r\n\r\n{disp}"

    else:
        chat_collection.insert_one(
            {"username": "Guest", "message": the_message, 'identification': 0, "image": the_image})
        print("I inserted into chat_collect")
        # Updating Code for the AO
        # body = {"username": "Guest", "message": the_message, 'identification': 0, "image": the_image}
        # body = json.dumps(body)
        # response = f"HTTP/1.1 201 Created\r\nX-Content-Type-Options: nosniff\r\n\r\n{body}"
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

