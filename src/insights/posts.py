from src.services.db_services import COMMENTS

def get_list_of_all_posts(page_number, 
                  documents_per_page,
                  post_search_query,
                  sentiment):
  
  match_query = {}
  
  if post_search_query and post_search_query.strip():
      match_query["post_title"] = {
          "$regex": post_search_query,
          "$options": "i"  # Case-insensitive search
      }
      
  if sentiment:
      match_query["sentiment"] = sentiment.capitalize()
  
  group_pipeline = [
      {
          "$match": match_query
      },
      {
          "$group": {
              "_id": "$post_id",
              "total_posts": {"$sum": 1}
          }
      },
      {
          "$project": {
              "_id": 0,
              "total_posts": 1
          }
      }
  ]
  
  group_result = list(COMMENTS.aggregate(group_pipeline))
  
  total_docs = len(group_result)
  num_pages = (total_docs + documents_per_page - 1) // documents_per_page
  
  pipeline = [
      {
          "$match": match_query
      },
      {
          "$sort": {
              "created_at": -1
          }
      },
      {
          "$group": {
              "_id": "$post_id",
              "post_title": {"$first": "$post_title"},
              "created_at": {"$first": "$created_utc"},
              "subreddit": {"$first": "$subreddit"},
              "comment_count": {"$sum": 1},  # Count the number of comments for each post_id
              "sentiment_counts": {
                  "$push": "$sentiment"  # Collect all sentiments for this post_id
              }
          }
      },
      {
          # Map sentiment counts into key-value pairs
          "$project": {
              "_id": 0,
              "post_id": "$_id",
              "post_title": 1,
              "subreddit": 1,
              "created_at": 1,
              "comment_count": 1,
              "sentiment_breakdown": {
                  "$arrayToObject": {
                      "$map": {
                          "input": {"$setUnion": ["$sentiment_counts", []]},  # De-duplicate sentiments
                          "as": "sentiment",
                          "in": {
                              "k": "$$sentiment",
                              "v": {
                                  "$size": {
                                      "$filter": {
                                          "input": "$sentiment_counts",
                                          "as": "item",
                                          "cond": {"$eq": ["$$item", "$$sentiment"]}
                                      }
                                  }
                              }
                          }
                      }
                  }
              }
          }
      },
      {
          # Sort the sentiment breakdown and find the trending sentiment
          "$addFields": {
              "trending_sentiment": {
                  "$arrayElemAt": [
                      {
                          "$map": {
                              "input": {
                                  "$sortArray": {
                                      "input": {
                                          "$objectToArray": "$sentiment_breakdown"
                                      },
                                      "sortBy": {"v": -1}  # Sort descending by count
                                  }
                              },
                              "as": "pair",
                              "in": "$$pair.k"  # Get the sentiment key
                          }
                      },
                      0  # First element is the trending sentiment
                  ]
              }
          }
      },
      {
          "$sort": {
              "created_at": -1  # Sort by post_date after grouping
          }
      },
      {
          "$skip": documents_per_page * (page_number - 1)
      },
      {
          "$limit": documents_per_page
      }
  ]
  try:
      docs = list(COMMENTS.aggregate(pipeline))
      
      return {
          "current_page": page_number,
          "total_pages": num_pages,
          "total_documents": total_docs,
          "documents": docs
      }
  
  except Exception as e:
      return "Error fetching posts: " + str(e)
  
  
def get_comments_by_post_id(post_id, page_number, documents_per_page):
  try:
    match_query = {
        "post_id": post_id
        
        }
        
        # if sentiment:
        #     match_query["sentiment"] = sentiment.capitalize()
            
        # if user_search_query and user_search_query.strip():
        #     match_query["user_name"] = {
        #         "$regex": user_search_query, 
        #         "$options": "i"
        #     }

    total_docs = COMMENTS.count_documents(match_query)
    num_pages = (total_docs + documents_per_page - 1) // documents_per_page  

    pipeline = [
    {
        "$match": match_query
    },
    {
        "$sort": {
            "insert_time": -1
        }
    },
    {
        "$project": {
            "_id": 0,
            # "user_id": 1,
            "post_id": 1,
            "post_title": 1,
            "author": 1,
            "body": 1,
            "sentiment": 1,
            "created_utc": 1
        }
    },
    {
        "$skip": documents_per_page * (page_number - 1)
    },
    {
        "$limit": documents_per_page
    }
    ]
    
    docs = list(COMMENTS.aggregate(pipeline))    
    return {
        "current_page": page_number,
        "total_pages": num_pages,
        "total_documents": total_docs,
        "documents": docs
    }
  except Exception as e:
      return "Error fetching comments: " + str(e)
  
def get_chart_data_from_post_id(post_id):
    
    try:
        
        match_query = {
            "post_id": post_id
        }
        
        pipeline = [
        {
            "$match": match_query
        },
        {
            "$group": {
                "_id": "$sentiment",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort":{
            "count": -1
            }
        },
        {
            "$project": {
                "sentiment": "$_id",
                "count": 1,
                "_id": 0
            }
        }
        ]
    
        total_comments = COMMENTS.count_documents(match_query)
        sentiment_result = list(COMMENTS.aggregate(pipeline))
        
        existing_sentiments = ["Satisfied", "Dissatisfied", "Sarcastic", "Curious", "Neutral", "Sad", "Profanity"]
        for sentiment in existing_sentiments:
            if sentiment.lower() not in {entry["sentiment"].lower() for entry in sentiment_result}:
                        sentiment_result.append({"count": 0, "sentiment": sentiment})
            
            # trending_sentiment = sentiment_result[0].get("sentiment", "NA")
            
            # post_details = {
            #     "post_id": post_id,
            #     "post_title": post_title,
            #     "post_caption": post_caption,
            #     "post_date": post_date,
            #     "total_comments": total_comments,
            #     "trending_sentiment": trending_sentiment,
            #     "sentiment_distribution": sentiment_result
            # }
        
        return sentiment_result
    except Exception as e:
        return "Error fetching post details: " + str(e)