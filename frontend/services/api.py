import requests

API_URL = "http://127.0.0.1:8000"

def login_user(email, password):
    return requests.post(
        f"{API_URL}/users/login",
        json={"email": email, "password": password}
    )

def register_user(name, email, password):
    return requests.post(
        f"{API_URL}/users/register",
        json={"name": name, "email": email, "password": password}
    )

def upload_clothing(file, user_id, item_name, category, subcategory, color, season, occasion):
    files = {
        "file": (file.name, file, file.type)
    }

    data = {
        "user_id": user_id,
        "item_name": item_name,
        "category": category,
        "subcategory": subcategory,
        "color": color,
        "season": season,
        "occasion": occasion
    }

    response = requests.post(
        f"{API_URL}/clothes/upload",
        files=files,
        data=data
    )

    if response.status_code == 200:
        return response.json()

    print("Upload error:", response.status_code, response.text)
    return None

def get_clothes(user_id):
    response = requests.get(
        f"{API_URL}/clothes/",
        params={"user_id": user_id}
    )

    if response.status_code == 200:
        return response.json()

    print("Error getting clothes:", response.status_code, response.text)
    return []

def save_outfit(user_id, name, clothing_item_ids):
    response = requests.post(
        f"{API_URL}/outfits/",
        json={
            "user_id": user_id,
            "name": name,
            "clothing_item_ids": clothing_item_ids
        }
    )

    if response.status_code == 200:
        return response.json()

    print("Error saving outfit:", response.status_code, response.text)
    return None

def update_clothing_item(item_id, item_name, category, subcategory, color, season, occasion):
    data = {
        "item_name": item_name,
        "category": category,
        "subcategory": subcategory,
        "color": color,
        "season": season,
        "occasion": occasion
    }

    response = requests.put(f"{API_URL}/clothes/{item_id}", data=data)

    if response.status_code == 200:
        return response.json()

    print("Update error:", response.status_code, response.text)
    return None

def delete_clothing_item(item_id):
    response = requests.delete(f"{API_URL}/clothes/{item_id}")

    if response.status_code == 200:
        return response.json()

    print("Delete error:", response.status_code, response.text)
    return None

def get_saved_outfits(user_id):
    response = requests.get(
        f"{API_URL}/outfits/",
        params={"user_id": user_id}
    )

    if response.status_code == 200:
        return response.json()

    print("Get outfits error:", response.status_code, response.text)
    return []


def delete_outfit(outfit_id):
    response = requests.delete(f"{API_URL}/outfits/{outfit_id}")

    if response.status_code == 200:
        return response.json()

    print("Delete outfit error:", response.status_code, response.text)
    return None