from loguru import logger
from app.forums.reddit.reddit_client import reddit_client as reddit
from asyncpraw.models import MoreComments
from app.config import REDDIT_SECOND_LEVEL_COMMENTS_LIMIT , REDDIT_TOP_LEVEL_COMMENTS_LIMIT


async def extract_comments_from_single_post(post_url: str):

    logger.debug(f"post_id={post_url}")
    submission = await reddit.submission(url=post_url)

    comments = await submission.comments()

    comments_output = []

    for top_level_comment in comments:
        if len(comments_output) > REDDIT_TOP_LEVEL_COMMENTS_LIMIT:
            break
        if(isinstance(top_level_comment , MoreComments)):
            continue
        comment = top_level_comment.body
        replies = []
        for second_level_comment in top_level_comment.replies:
            if len(replies) > REDDIT_SECOND_LEVEL_COMMENTS_LIMIT:
                break
            if (isinstance(second_level_comment ,MoreComments)):
                continue
            replies.append(second_level_comment.body)
        comments_output.append({"comment": comment, "replies": replies})

    return {"comments_output": comments_output , "post_title" : submission.title}
