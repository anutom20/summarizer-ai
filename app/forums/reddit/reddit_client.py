import asyncpraw
from app.config import REDDIT_CLIENT_ID , REDDIT_CLIENT_SECRET , REDDIT_USER_AGENT

reddit_client = asyncpraw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

