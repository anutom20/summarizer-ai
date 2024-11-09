from fastapi import APIRouter, HTTPException, status
from app.forums.stackoverflow.stack_overflow_client import stackoverflow_client as SITE
from loguru import logger
from app.common import GeminiPrompt
from app.gemini import get_stack_exchange_prompt_single_question , generate_summary
from app.config import STACKOVERFLOW_ANSWERS_FILTER_VALUE , STACKOVERFLOW_QUESTIONS_FILTER_VALUE , STACKOVERFLOW_COMMENTS_FILTER_VALUE

router = APIRouter(prefix='/stackAPI' , tags=["Stack API"])

@router.get("/get_questions")
def get_questions_from_queries(search_term : str):
    try:
        questions = SITE.fetch('search/advanced', fromdate=1457136000, q=search_term, sort='relevance' , filter=STACKOVERFLOW_QUESTIONS_FILTER_VALUE, pagesize=20 , page=1)
        return questions

    except Exception as e:
        logger.error(f"An exception occured while getting stackoverflow questions = {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"{e}")


@router.get("/get_answers")
def get_answers_from_question(question_id : int):
    try:
        answers = SITE.fetch('questions/{ids}/answers' , ids=[question_id] , filter=STACKOVERFLOW_ANSWERS_FILTER_VALUE)
        return answers

    except Exception as e:
        logger.error(f"An exception occured while getting stackoverflow answers = {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"{e}")



@router.get("/generate_answers_summary")
async def generate_answers_summary(question_id : int):
    try:
        answers = SITE.fetch('questions/{ids}/answers' , ids=[question_id] , filter=STACKOVERFLOW_ANSWERS_FILTER_VALUE)

        answer_ids = [answer['answer_id'] for answer in answers['items']]

        logger.debug(f"{answer_ids=}")

        comments = SITE.fetch('answers/{ids}/comments' , ids=answer_ids , filter=STACKOVERFLOW_COMMENTS_FILTER_VALUE)

        gemini_prompt_string = get_stack_exchange_prompt_single_question(answers=answers['items'] , comments=comments['items'])

        logger.info(f"{gemini_prompt_string}=")

        gemini_prompt = GeminiPrompt(question=gemini_prompt_string)

        llm_res = await generate_summary(gemini_prompt=gemini_prompt)
        
        return llm_res


    except Exception as e:
        logger.error(f"An expection occured while generating stack summary = {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"{e}")

    