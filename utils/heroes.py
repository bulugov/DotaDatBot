import json
import os
import requests
from PIL import Image

HEROES_PATH = "heroes.json"
ICON_DIR = "hero_icons"
os.makedirs(ICON_DIR, exist_ok=True)

hero_dict = {}


def load_hero_dict():
    global hero_dict
    if not hero_dict:
        with open(HEROES_PATH) as f:
            data = json.load(f)
            hero_dict.update({h["id"]: h["localized_name"] for h in data})
    return hero_dict


def get_hero_icon(hero_name):
    file_name = hero_name.lower().replace(" ", "_").replace("-", "") + "_full.png"
    file_path = os.path.join(ICON_DIR, file_name)

    if not os.path.exists(file_path):
        url = f"https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heroes/{file_name}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            return None
    return Image.open(file_path).resize((64, 36))
