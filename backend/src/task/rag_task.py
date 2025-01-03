from celery import shared_task
from utils import setup_logging
import logging
from src.rag.rag_flow import bot_rag_answer_message

setup_logging()
logger = logging.getLogger(__name__)

@shared_task() 
def bot_rag_home_loan_faq_answer_message(history, message):
    return bot_rag_answer_message(history, message)[0]