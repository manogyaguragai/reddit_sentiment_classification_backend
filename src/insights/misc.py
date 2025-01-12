from src.services.db_services import COMMENTS

def get_all_subreddits():
  subreddits = COMMENTS.distinct("subreddit")
  return subreddits

def get_all_sentiments():
  sentiments = COMMENTS.distinct("sentiment")
  return sentiments