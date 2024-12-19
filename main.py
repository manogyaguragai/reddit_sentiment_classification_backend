from fastapi import FastAPI, HTTPException 
from fastapi.responses import RedirectResponse
from fetch_comments import fetch_comments

app = FastAPI(title = "Reddit Comments Sentiment Classifier", version="1.0.0")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/fetch_comments/subreddit")
async def fetch_comments_from_subreddit(subreddit: str, limit: int = 100):
    try:
        if limit <= 0:
            raise HTTPException(status_code = 400, detail = "Limit must be greater than 0.")
        
        await fetch_comments(subreddit, limit)
        return {"status": "success", "message": f"Comments from subreddit '{subreddit}' successfully fetched and stored."}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch comments: {str(e)}")
