from fastapi import APIRouter, HTTPException, status
from app.forums.reddit.reddit_client import reddit_client as reddit
from loguru import logger
from app.common import GeminiPrompt
from app.utils import extract_comments_from_single_post
import asyncio
from app.gemini import generate_summary, get_reddit_summary_prompt_single_post
from app.config import REDDIT_SEARCH_RESULTS_LIMIT


router = APIRouter(prefix="/api", tags=["Reddit"])


@router.get("/get_posts_by_query")
async def get_posts(question: str):
    try:
        all_subreddit = await reddit.subreddit("all")

        posts_info = [
            post
            async for post in all_subreddit.search(
                question, limit=REDDIT_SEARCH_RESULTS_LIMIT
            )
        ]

        logger.debug(f"{posts_info=}")

        return {"posts_info": posts_info, "total_count": len(posts_info)}

    except Exception as e:
        logger.error(f"An exception occured while getting posts={e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.get("/get_post_comments")
async def extract_comments(post_url: str):
    try:
        comments = await extract_comments_from_single_post(post_url=post_url)

        return comments

    except Exception as e:
        logger.error(f"exception while fetching comments = {e}")


@router.get("/generate_summary_single_post")
async def generate_summary_single_post(post_url: str):
    try:
        comments = await extract_comments_from_single_post(post_url=post_url)

        prompt_string = get_reddit_summary_prompt_single_post(
            reddit_comments=comments["comments_output"],
            post_title=comments["post_title"],
        )

        geminiPrompt = GeminiPrompt(question=prompt_string)

        llm_res = generate_summary(geminiPrompt=geminiPrompt)

        return llm_res

    except Exception as e:
        logger.error(f"exception while generating summary = {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
