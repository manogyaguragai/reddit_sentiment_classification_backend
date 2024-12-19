import json
from pymongo import MongoClient

def load_config(file_path):
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Load configuration
config_path = "config.json"
config = load_config(config_path)

if config:
    CLIENT_ID = config.get("client_id")
    CLIENT_SECRET = config.get("client_secret")
    USERNAME = config.get("username")
    PASSWORD = config.get("password")
    MONGO_URI = config.get("mongo_uri")

    # MongoDB setup
    client = MongoClient(MONGO_URI)
    DB = client["RedditSentimentProject"]
    COMMENTS = DB["comments"]
