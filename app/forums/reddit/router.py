from fastapi import APIRouter, HTTPException, status
from app.forums.reddit.reddit_client import reddit_client as reddit
from loguru import logger
from app.common import GeminiPrompt
from app.forums.reddit.utils import extract_comments_from_single_post
from app.gemini import generate_summary, get_reddit_summary_prompt_single_post
from app.config import REDDIT_SEARCH_RESULTS_LIMIT
from app.forums.reddit.utils import get_fuzzy_matches
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/reddit", tags=["Reddit"])


@router.get("/get_posts_by_query")
async def get_posts(question: str, keyphrase: str):
    try:
        all_subreddit = await reddit.subreddit("all")

        posts_info = [
            {"title": post.title, "url": post.url}
            async for post in all_subreddit.search(
                question, limit=REDDIT_SEARCH_RESULTS_LIMIT
            )
        ]

        posts_info = get_fuzzy_matches(query=keyphrase, data=posts_info)

        return {"posts": posts_info, "total_count": len(posts_info)}

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.get("/generate_summary_single_post")
async def generate_summary_single_post(post_url: str):
    try:
        comments = await extract_comments_from_single_post(post_url=post_url)

        prompt_string = get_reddit_summary_prompt_single_post(
            reddit_comments=comments["comments_output"],
            post_title=comments["post_title"],
        )

        gemini_prompt = GeminiPrompt(question=prompt_string)

        llm_res = generate_summary(gemini_prompt=gemini_prompt)

        return StreamingResponse(content=llm_res, media_type="text/plain")

    except Exception as e:
        logger.error(f"exception while generating summary = {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


@router.get("/generate_summary_prompt")
async def generate_summary_single_post(post_url: str):
    try:
        comments = await extract_comments_from_single_post(post_url=post_url)

        prompt_string = get_reddit_summary_prompt_single_post(
            reddit_comments=comments["comments_output"],
            post_title=comments["post_title"],
        )

        gemini_prompt = GeminiPrompt(question=prompt_string)

        return gemini_prompt

    except Exception as e:
        logger.error(f"exception while generating summary = {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )
