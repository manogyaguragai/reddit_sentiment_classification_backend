# Reddit Comments Sentiment Classifier

This repository contains a **FastAPI**-based backend service that fetches, processes, and provides insights into Reddit comments and posts. It supports fetching comments from specific subreddits or Reddit post URLs and analyzing sentiment to generate useful insights.

## Features

- **Fetch Comments:** Retrieve comments from specific subreddits or individual post URLs.
- **Pagination Support:** Navigate through posts and their comments with pagination.
- **Sentiment Filtering:** Filter posts based on sentiment categories.
- **Data Insights:** Generate sentiment analysis data for posts in chart format.
- **Interactive API Docs:** Explore and test API endpoints via an automatically generated Swagger UI.

## Endpoints

### 1. Root Endpoint
- **URL:** `/`
- **Description:** Redirects to `/docs` for interactive API documentation.

### 2. Fetch Comments from Subreddit
- **Method:** `POST`
- **URL:** `/fetch_comments/subreddit`
- **Parameters:**
  - `subreddit` (str, required): The name of the subreddit.
  - `limit` (int, optional): Maximum number of comments to fetch (default: 100).
- **Response:** Status message indicating success or failure.

### 3. Fetch Comments from URL
- **Method:** `POST`
- **URL:** `/fetch_comments/url`
- **Parameters:**
  - `url` (str, required): Reddit post URL.
  - `limit` (int, optional): Maximum number of comments to fetch (default: 100).
- **Response:** Status message indicating success or failure.

### 4. Get All Posts
- **Method:** `GET`
- **URL:** `/posts/all`
- **Parameters:**
  - `page_number` (int, optional): Page number for pagination (default: 1).
  - `documents_per_page` (int, optional): Number of posts per page (default: 10).
  - `post_search_query` (str, optional): Search query to filter posts.
  - `sentiment` (str, optional): Filter posts by sentiment.
- **Response:** Paginated list of posts.

### 5. Get Post Details by ID
- **Method:** `GET`
- **URL:** `/posts/{post_id}`
- **Parameters:**
  - `post_id` (str, required): ID of the post.
  - `page_number` (int, optional): Page number for pagination (default: 1).
  - `documents_per_page` (int, optional): Number of comments per page (default: 10).
- **Response:** Paginated list of comments for the specified post.

### 6. Get Chart Data for a Post
- **Method:** `GET`
- **URL:** `/posts/{post_id}/chart`
- **Parameters:**
  - `post_id` (str, required): ID of the post.
- **Response:** Chart data representing sentiment analysis of the post.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/manogyaguragai/reddit_sentiment_classification_backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd reddit_sentiment_classification_backend
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Running the Application
1. Start the server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
2. Access the Swagger UI at http://127.0.0.1:8000/docs to explore and test the API.

## Contributing
Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.


  
