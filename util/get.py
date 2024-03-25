import json
import base64


def chat_messages(chat_collection):
    response = []
    for chat in chat_collection.find():
        response_dict = {"messageType": 'chatMessage', "username": chat["username"], "message": chat["message"],
                         "id": chat["identification"], "img": chat["image"], "upv": chat["Upvote"], "dwv": chat["Downvote"]}  # "id": chat["_id"],
        image_data = base64.b64encode(chat["image"]).decode("utf-8")
        response_dict["img"] = image_data
        # removes key value pair id
        response_dict.pop("_id", "")
        response.append(response_dict)
    # research
    j = json.dumps(response)
    return j


class Get:

    def __init__(self, request_path, chat_collection, user_collection):
        self.response = ""
        if '/chat-message' in request_path:
            print("i AM IN chat MESSAGES")
            self.response = chat_messages(chat_collection)



