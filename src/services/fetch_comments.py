import asyncpraw
from models import RedditComment
from pydantic import ValidationError
from fastapi import APIRouter
from src.services.get_sentiment import get_sentiment
from datetime import datetime
from src.services.db_services import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, COMMENTS

# Async PRAW setup
reddit = asyncpraw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="RedditSentimentAnalyzer",
    username=USERNAME,
    password=PASSWORD,
)

# Define FastAPI router
router = APIRouter()

async def fetch_comments_sub(subreddit_name: str, limit: int = 100):
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
            COMMENTS.update_one(
                {"id": reddit_comment.id},
                {"$set": reddit_comment.dict()},
                upsert=True,
            )
            print(f"Inserted or updated comment with ID: {reddit_comment.id}")

        except ValidationError as e:
            print(f"Validation error for comment {comment.id}: {e}")
        except Exception as e:
            print(f"Error for comment {comment.id}: {e}")
            
async def fetch_comments_url(post_url: str, limit: int = 100):
    """Fetch all comments from a URL using Async PRAW and save to MongoDB."""
    
    submission = await reddit.submission(url=post_url)
    post_title = submission.title
    
    async for comment in submission.comments:
        
        try:
            reddit_comment = RedditComment(
                id=comment.id,
                author=comment.author.name if hasattr(comment, 'author') and comment.author else None,
                subreddit=str(comment.subreddit),
                body=str(comment.body),
                post_id=comment.parent_id,
                post_title=post_title,  # link_id as there is no post_title in your provided fields
                post_author=comment.link_author if hasattr(comment, 'link_author') and comment.link_author else None,
                post_permalink=f"https://www.reddit.com{comment.permalink}",  # Use permalink directly
                created_utc=comment.created_utc,
                score=comment.score,
                comment_permalink=f"https://www.reddit.com{comment.permalink}",
                parent_id=comment.parent_id,
                edited=bool(comment.edited),
                sentiment=None,
                insert_time=datetime.now()
            )


            sentiment = get_sentiment(comment.body)
            reddit_comment.sentiment = sentiment
        
            # Insert or update in MongoDB
            COMMENTS.update_one(
                {"id": reddit_comment.id},
                {"$set": reddit_comment.dict()},
                upsert=True,
            )
            print(f"Inserted or updated comment with ID: {reddit_comment.id}")

        except ValidationError as e:
            print(f"Validation error for comment {comment.id}: {e}")
        except Exception as e:
            print(f"Error for comment {comment.id}: {e}")