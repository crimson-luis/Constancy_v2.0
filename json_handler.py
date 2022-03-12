import json
import common as cm
import os
import regex as re


def user_exists(loc):
    """Returns True if the given file/user exists and False else."""
    try:
        with open(loc, "r") as file:
            return True
    except IOError:
        return False


def write_file(loc, json_str):
    """Opens or creates the file and writes the given encrypted
    (cryptography.fernet.Fernet) json string to it."""
    with open(loc, "wb+") as js:
        f = cm.get_key()
        token = f.encrypt(json.dumps(json_str).encode())
        js.write(token)


def get_info(loc):
    """Returns a tuple with a dictionary of the owner information and the id of the last
    item (or the number of items)"""
    with open(loc, "rb") as js:
        js_file = js.read()
    f = cm.get_key()
    user_json_decrypted = f.decrypt(js_file).decode()
    data_dic = json.loads(user_json_decrypted)
    user_items_last_id = len(data_dic["items"])
    return data_dic, user_items_last_id


def get_users():
    """Returns a tuple with a dictionary of all users and their id's and a variable that
    refers to the number of files/users."""
    _files = []
    users_ids = dict()
    id_count = 0
    for filenames in os.walk(cm.resource_path("")):
        _files.extend(filenames)
        break
    for item in _files[2]:
        if re.search(".encrypted", item):
            try:
                _info = get_info(cm.resource_path(item))
                users_ids[_info[0]["user"]["name"]] = _info[0]["user"]["id"]
                id_count = id_count + 1
            except TypeError:
                pass
    return users_ids, id_count


def create_sub_item():
    """Talvez não precise."""
    pass


def create_item(dic, description, value, date, installments, _type, sub_items=None):
    """Returns a dictionary with all user information including the new item that it
    creates. If sub_items is given then create_sub_item function is called."""
    last_item_id = len(dic["items"])
    new_item = {
        "item_id": last_item_id,
        "description": description,
        "value": value,
        "date": date,
        "installments": installments,
        "type": _type,
        "sub_items": sub_items,
    }
    # if sub_items is None:
    dic["items"].append(new_item)
    return dic


def create_user(name, password, email, loc):
    """Creates a dictionary with all information given, calls create_item function to
    create the first user item and saves the user file (name.encrypted)."""
    dic = {
        "user": {
            "id": get_users()[1] + 1,
            "name": name,
            "password": password,
            "email": email,
            "settings": {
                "theme": 0,
                "lang": "pt_br",
                "eyes": True,
                "save": False,
                "repass": False,
            },
        },
        "items": [],
    }
    create_item(dic, "Saldo Inicial", 0, "-/-/-", 1, 1)
    write_file(loc, dic)
