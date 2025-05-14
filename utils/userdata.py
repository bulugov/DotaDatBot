import json
import os

USERDATA_FILE = "user_links.json"


def load_user_links():
    if os.path.exists(USERDATA_FILE):
        with open(USERDATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_user_links(data):
    with open(USERDATA_FILE, "w") as f:
        json.dump(data, f)


def link_user(telegram_id, dota_account_id):
    data = load_user_links()
    data[str(telegram_id)] = dota_account_id
    save_user_links(data)


def get_linked_account(telegram_id):
    data = load_user_links()
    return data.get(str(telegram_id))
