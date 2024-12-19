import asyncpraw
import json
from models import RedditComment
from pydantic import ValidationError
from pymongo import MongoClient
from fastapi import APIRouter
from get_sentiment import get_sentiment
from datetime import datetime

# Load configuration from JSON file
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
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    username = config.get("username")
    password = config.get("password")
    mongo_uri = config.get("mongo_uri")

    # MongoDB setup
    client = MongoClient(mongo_uri)
    db = client["RedditSentimentProject"]
    comments_collection = db["comments"]

# Async PRAW setup
reddit = asyncpraw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="RedditSentimentAnalyzer",
    username=username,
    password=password,
)

# Define FastAPI router
router = APIRouter()

async def fetch_comments(subreddit_name: str, limit: int = 100):
    """Fetch comments from a subreddit using Async PRAW and save to MongoDB."""
    subreddit = await reddit.subreddit(subreddit_name)
    async for comment in subreddit.comments(limit=limit):
        try:
            reddit_comment = RedditComment(
                id = comment.id,
                author = comment.author.name if comment.author else None,
                subreddit = str(comment.subreddit.display_name),
                body = str(comment.body),
                post_id = comment.link_id,
                post_title = comment.link_title,
                post_author = comment.link_author if comment.link_author else None,
                post_permalink = comment.link_permalink,
                created_utc = comment.created_utc,
                score = comment.score,
                comment_permalink = f"https://www.reddit.com{comment.permalink}",
                parent_id = comment.parent_id,
                edited = bool(comment.edited),
                sentiment = None,
                insert_time = datetime.now()
            )
            
            sentiment = get_sentiment(comment.body)
            reddit_comment.sentiment = sentiment
        
            # Insert or update in MongoDB
            comments_collection.update_one(
                {"id": reddit_comment.id},
                {"$set": reddit_comment.dict()},
                upsert=True,
            )
            print(f"Inserted or updated comment with ID: {reddit_comment.id}")

        except ValidationError as e:
            print(f"Validation error for comment {comment.id}: {e}")
        except Exception as e:
            print(f"Error for comment {comment.id}: {e}")