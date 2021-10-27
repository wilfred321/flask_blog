from datetime import datetime, date
from pathlib import Path
import json


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def save_user(filename, user):
    with open(filename, "a") as file:
        file.write(f"{user.username}, {user.email}, {datetime.now()} \n")


saved_users = []


def save_user_json(filename, user):

    user_info = {
        "username": user.username,
        "user_email": user.email,
        "date_created": datetime.now(),
    }
    saved_users.append(user_info)
    data = json.dumps(saved_users, default=json_serial)
    with open(filename, "w") as f:
        f.write(data)


def extract_users(filename, mode="r"):
    with open(filename, mode) as file:
        data = json.loads(file.read())
    return data