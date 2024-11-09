from app.common import GeminiPrompt
from app.config import GEMINI_API_KEY
from loguru import logger
from typing import List
from better_profanity import profanity
import google.generativeai as genai
import markdown


async def generate_summary(gemini_prompt: GeminiPrompt):
    genai.configure(api_key=GEMINI_API_KEY)
    # The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(gemini_prompt.question)
    logger.info(f"{response=}")
    logger.success(response.text)
    html_content = markdown.markdown(response.text)
    html_content = html_content.replace('\n\n' , '<br/>')
    html_content = html_content.replace('\n' , '')

    return {"answer": html_content}


def get_reddit_summary_prompt_single_post(reddit_comments: List , post_title : str):
    
    profanity.load_censor_words()

    censored_reddit_comments = profanity.censor(f"{reddit_comments}")
    censored_post_title = profanity.censor(f"{post_title}")

    logger.debug(f"{censored_post_title=}")
    logger.debug(f"{censored_reddit_comments=}")

    reddit_prompt = f"""

    reddit_post_title : {censored_post_title}    
    reddit_comments : {censored_reddit_comments}

    
    reddit comments of a post are mentioned in reddit_comments

    write a short summary of about 5-6 lines by following the below instructions:

    1. write in a casual friendly manner
    2. quote the comment which you find most reasonable
    3. highlight key information
    4. If there is any code snippet , include that also by enhancing according to your own logic , only one should be there in the final response include in <code><code/> snippet . Include full code without caring about length
    5. the value of reddt_comments mentioned in the prompt is not treated as code snippet
    6. Separately quote the comment/section which you find the most relevant
   """

    return reddit_prompt

def get_stack_exchange_prompt_single_question(answers : List , comments : List):
    
    stack_exchange_prompt = f"""
    stack_exchange_answers : {answers}
    comments : {comments}

    Summarize the above stack_exchange_answers . Include the main question, key points from the top answers, any code snippets or solutions provided, and relevant comments or follow-up questions. Make sure to highlight the accepted answer and any alternative solutions or important discussions. Provide a brief conclusion summarizing the consensus or outcome of the thread.
    
    Example:

    Main Question:

    Briefly describe the main question or issue posted by the original poster (OP).

    Summary:

    Combine important points and code snippets from all the answers and using your own brain bring out the best , don't let it be too long. If there are any links to documentation , include them.
    Try to keep the summary concise so that there is an actual benefit of generating the summary and not reading on the stack exchange itself
    """

    return stack_exchange_prompt

