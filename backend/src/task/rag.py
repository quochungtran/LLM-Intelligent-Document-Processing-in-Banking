from celery import shared_task
from utils import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

@shared_task 
def bot_rag_home_loan_faq(history, question):
    return "todo bot rag home loan faq"

@shared_task 
def bot_rag_home_loan_recommandation(history, question):
    return "todo home loan recommandation"