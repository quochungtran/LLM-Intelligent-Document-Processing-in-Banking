from celery import shared_task
from utils import setup_logging
from models import *
from brain import openai_chat_complete
from src.task.rag_task import bot_rag_home_loan_faq_answer_message
from src.task.agent_task import bot_agent_home_loan_recommandation_answer_message
from src.brain import detect_route
import logging

setup_logging()
logger = logging.getLogger(__name__)

@shared_task()
def bot_route_answer_message(history, question):
    # detect the route
    route = detect_route(history, question)
    if route == 'home_loan_faq':
        return bot_rag_home_loan_faq_answer_message(history, question)
    elif route == 'home_loan_recommandation':
        return bot_agent_home_loan_recommandation_answer_message(history, question)
    else:
        return "Sorry, I don't understand your question."

@shared_task()
def llm_handle_message(bot_id, user_id, question):
    logger.info("Start handle message")
    # Update chat conversation  
    conversation_id = update_chat_conversation(bot_id, user_id, question, True)
    logger.info("Conversation id: %s", conversation_id)
    # Convert history to list messages given the conversation id
    messages = get_conversation_messages(conversation_id)
    logger.info("Conversation messages: %s", messages)
    history = messages[:-1]
    # Use bot route to handle
    response = bot_route_answer_message(history, question)
    logger.info(f"Chatbot response: {response}")
    # Save response to history
    update_chat_conversation(bot_id, user_id, response, False)
    # Return response
    return {"role": "assistant", "content": response}