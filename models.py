from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RedditComment(BaseModel):
    id: str
    author: Optional[str]
    subreddit: str
    body: str
    post_id: Optional[str]
    post_title: Optional[str]
    post_author: Optional[str]
    post_permalink: Optional[str]
    created_utc: Optional[datetime]
    score: Optional[int]
    comment_permalink: Optional[str]
    parent_id: Optional[str]
    edited: Optional[bool]
    sentiment: Optional[str]
    insert_time: datetime