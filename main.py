from fastapi import FastAPI, HTTPException 
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.services.fetch_comments import fetch_comments_sub, fetch_comments_url
from src.insights.posts import get_list_of_all_posts, get_comments_by_post_id, get_chart_data_from_post_id
from src.insights.misc import get_all_subreddits, get_all_sentiments
from typing import Optional

app = FastAPI(title = "Reddit Comments Sentiment Classifier", version="1.0.0")

# allow_origins = ["http://localhost:3000"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/fetch_comments/subreddit")
async def fetch_comments_from_subreddit(subreddit: str, limit: int = 100):
    try:
        if limit <= 0:
            raise HTTPException(status_code = 400, detail = "Limit must be greater than 0.")
        
        await fetch_comments_sub(subreddit, limit)
        return {"status": "success", "message": f"Comments from subreddit '{subreddit}' successfully fetched and stored."}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch comments: {str(e)}")
    

@app.post("/fetch_comments/url")
async def fetch_comments_from_url(url: str, limit: int = 100):
    try:
        if limit <= 0:
            raise HTTPException(status_code = 400, detail = "Limit must be greater than 0.")
        
        await fetch_comments_url(url, limit)
        return {"status": "success", "message": f"Comments from URL '{url}' successfully fetched and stored."}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch comments: {str(e)}")
    
@app.get("/posts/all")
async def get_all_posts(page_number: int = 1, 
                        documents_per_page: int = 10,
                        post_search_query: Optional[str] = None,
                        sentiment: Optional[str] = None,
                        subreddit: Optional[str] = None
                        ):
    
    try:
        return get_list_of_all_posts(page_number, documents_per_page, post_search_query, sentiment, subreddit)
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch posts: {str(e)}")
    
@app.get("/posts/{post_id}")
async def get_post_details_by_id(post_id: str, page_number: int = 1, documents_per_page: int = 10):
    try:
        return get_comments_by_post_id(post_id, page_number, documents_per_page)
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch posts: {str(e)}")


@app.get("/posts/{post_id}/chart")
async def get_chart_data(post_id: str):
    
  try:
    return get_chart_data_from_post_id(post_id)
  except Exception as e:
    return "Error fetching post details: " + str(e)
  
@app.get("/subreddits")
async def get_all_subreddits_from_db():
    try:
        return get_all_subreddits()
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch subreddits: {str(e)}")
    
@app.get("/sentiments")
async def get_all_sentiments_from_db():
    try:
        return get_all_sentiments()
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch sentiments: {str(e)}")