from celery import shared_task
from utils import setup_logging
import logging
from src.agents.agents import bot_agent_home_loan_recommandation_handle

setup_logging()
logger = logging.getLogger(__name__)

@shared_task()
def bot_agent_home_loan_recommandation_answer_message(history, question):
    logger.info("Agent answer: {}".format(question))
    return bot_agent_home_loan_recommandation_handle(history, question)
