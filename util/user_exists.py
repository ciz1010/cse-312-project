import hashlib


def does_user_exist(request, user_collection):
    badaboom = request.cookies
    if (badaboom is not None) and (badaboom.get("Auth-Token") is not None):
        # print("There might be a user")
        auth_token = badaboom["Auth-Token"]
        hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
        user_exists = user_collection.find_one({"Auth-Token": hashed_auth_token}, {"_id": 0})
        # print("user_exists", user_exists)
    else:
        user_exists = None
    return user_exists


class User_Exists:

    def __init__(self, request, user_collection):
        self.user_exists = does_user_exist(request, user_collection)
