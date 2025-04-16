import requests
import json
import os

BASE_URL = "https://api.opendota.com/api"
HEROES_FILE = "heroes.json"

def rank_tier_to_name(rank_tier):
    if not rank_tier:
        return "Unranked"
    
    tiers = {
        1: "Herald",
        2: "Guardian",
        3: "Crusader",
        4: "Archon",
        5: "Legend",
        6: "Ancient",
        7: "Divine",
        8: "Immortal",
    }

    tier = rank_tier // 10
    star = rank_tier % 10

    rank_name = tiers.get(tier, "Unknown")
    return f"{rank_name} {star}" if tier < 8 else rank_name 

def fetch_and_save_heroes():
    response = requests.get(f"{BASE_URL}/heroes")
    if response.status_code == 200:
        hero_data = response.json()
        with open(HEROES_FILE, "w") as f: 
            json.dump(hero_data, f)
        return {hero["id"]: hero["localized_name"] for hero in hero_data}
    return {}

def get_hero_dict():
    if os.path.exists(HEROES_FILE):
        with open(HEROES_FILE, "r") as f:
            try:
                hero_data = json.load(f)
                return {hero["id"]: hero["localized_name"] for hero in hero_data}
            except json.JSONDecodeError:
                # Corrupt file or bad data — fallback to fetching again
                return fetch_and_save_heroes()
    else:
        return fetch_and_save_heroes()


def get_latest_match(account_id):
    response = requests.get(f"{BASE_URL}/players/{account_id}/recentMatches")
    return response.json()[0] if response.status_code == 200 else None

def get_player_info(account_id):
    response = requests.get(f"{BASE_URL}/players/{account_id}")
    return response.json() if response.status_code == 200 else None

def get_player_win_loss(account_id):
    response = requests.get(f"{BASE_URL}/players/{account_id}/wl")
    return response.json() if response.status_code == 200 else None
