from celery import shared_task
from utils import setup_logging
from models import *
from brain import openai_chat_complete
from src.task.rag_homeloan import bot_rag_home_loan_faq_answer_message
from src.task.agent import bot_agent_home_loan_recommandation_answer_message
import logging


setup_logging()
logger = logging.getLogger(__name__)

@shared_task()
def detect_route(history, message):
    logger.info(f"Detect route on history messages: {history}")

    user_prompt = f"""
    Given the following chat history and the user's latest message, determine whether the user's intent is to ask for a frequently asked question like
    provide general insights, trends, and FAQ responses about home loans ("home_loan_faq") \n
    or ("home_loan_recommandation") supporting approval/Reject Questions: Answer questions regarding specific home loan applications based on the loan data (e.g., approval status, missing requirements, loan recommendations).
    Provide only the classification label as your response \n.

    Chat History:
    {history}

    Latest User Message:
    {message}

    Classification (choose either "home_loan_faq" or "home_loan_recommandation" or "unknown"):
    """
    openai_messages = [
        {"role": "system", "content": "You are a highly intelligent assistant that helps classify customer queries"},
        {"role": "user", "content": user_prompt}
    ]
    
    logger.info(f"Route output: {openai_messages}")
    return openai_chat_complete(openai_messages)



@shared_task()
def bot_route_answer_message(history, question):
    # detect the route
    route = detect_route(history, question)
    if route == 'homeloan_faq':
        return bot_rag_home_loan_faq_answer_message(history, question)
    elif route == 'home_loan_recommandation':
        return bot_agent_home_loan_recommandation_answer_message(history, question)
    else:
        return "Sorry, I don't understand your question."


@shared_task
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