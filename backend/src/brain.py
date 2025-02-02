from openai import OpenAI
import logging
import json
from config import Config

logger = logging.getLogger(__name__)

def get_openai_client():
    return OpenAI(api_key=Config.OPENAI_API_KEY)

openai_client = get_openai_client()

def openai_chat_complete(messages=(), model="gpt-4o-mini", raw=False):
    logger.info("Chat complete for {}".format(messages))
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    if raw:
        return response.choices[0].message
    output = response.choices[0].message
    logger.info("Chat complete output: ".format(output))
    return output.content

def gen_doc_prompt(docs):
    """
    Document:
    Content: ....
    """
    doc_prompt = ""
    for doc in docs:
        doc_prompt += f"Content: {doc['content']} \n"

    return "Document: \n + {}".format(doc_prompt)

def summarize_home_loan_application(application_info, status):
    user_prompt = f"""
        You are an expert assistant specializing in financial topics, particularly home loans recommandation. 
        Summarize the home loan application of a user given the content:
        {json.dumps(application_info)} \n
        and predicted status of this application {status}
    """
    openai_messages = [
        {"role": "system", "content": "You are a highly intelligent assistant specializing in financial topics, specializing in home loan application recommandation"},
        {"role": "user", "content": user_prompt}
    ]
    summarized_homeloan_app = openai_chat_complete(openai_messages)
    logger.info(f"Home loan application summerize: {summarized_homeloan_app}")
    return summarized_homeloan_app

def summarize_doc_home_loan(doc_content):
    user_prompt = f"""
        You are an expert assistant specializing in financial topics, particularly home loans. 
        Summarize the text content below, ensuring it includes all relevant and important information about the text. 

        Ensure the summary is:
        - Concise, avoiding unnecessary repetition.
        - Well-organized using sections or bullet points for clarity.
        - Within the token limit of 8190.

        Text content:
        {doc_content}
    """
    openai_messages = [
        {"role": "system", "content": "You are a highly intelligent assistant specializing in financial topics, dedicated to providing actionable and clear insights about home loans."},
        {"role": "user", "content": user_prompt}
    ]
    summarized_txt = openai_chat_complete(openai_messages)
    logger.info("Home Loan Insights Summary: {summarized_txt}")
    return summarized_txt

def generate_conversation_text(conversations):
    conversation_text = ""
    for conversation in conversations:
        logger.info("Generate conversation: {}".format(conversation))
        role = conversation.get("role", "user")
        content = conversation.get("content", "")
        conversation_text += f"{role}: {content}\n"
    return conversation_text

def detect_user_intent(history, message):
    # Convert history to list messages
    history_messages = generate_conversation_text(history)
    logger.info(f"History messages: {history_messages}")
    # Update documents to prompt
    user_prompt = f"""
    Given following conversation and follow up question, rephrase the follow up question to a standalone question.

    Chat History:
    {history_messages}

    Original Question: {message}

    Answer:
    """
    openai_messages = [
        {"role": "system", "content": "You are an amazing virtual assistant"},
        {"role": "user", "content": user_prompt}
    ]
    logger.info(f"Rephrase input messages: {openai_messages}")
    # call openai
    return openai_chat_complete(openai_messages)

vectordb_collections = ['interest_rate', 'market_trends', 'eligibility', 'financial_choice', 'refinancing']

def detect_collection(history, message):
    history_messages = generate_conversation_text(history)

    user_prompt = f"""
    Given the following the user's latest message, determine whether the user's intent is to ask for with topic 
    {vectordb_collections}
    
    Chat History:
    {history_messages}

    Latest User Message:
    {message}

    Classification (choose one or more related topic amongs "interest_rate", "market_trends", "eligibility", "financial_choice", "refinancing"):
    Always return a list of topic, fox example:

    ["interest_rate","market_trends"]
    """
    openai_messages = [
        {"role": "system", "content": "You are a highly intelligent assistant that helps classify customer queries"},
        {"role": "user", "content": user_prompt}
    ]
    
    return openai_chat_complete(openai_messages)

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


finetune_model = "ft:gpt-4o-mini-2024-07-18:personal:homeloan-llm:An55Uasr"
def collect_homeloan_information(history, message):
    system_prompt = f"""
    Given the mandatory fields: \"name\", \"income\", \"loan_amount\", \"property_value\", \"loan_term\"(in months), and \"loan_purpose\", 
    Validate and collect missing or invalid fields.                
    Return a JSON object with the completed fields.
    """

    user_prompt = f"""
    Chat History:
    {history}

    Latest User Message:
    {message}
    """
    openai_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    logger.info(f"Home loan information output: {openai_messages}")
    return openai_chat_complete(openai_messages, model=finetune_model)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return openai_client.embeddings.create(input=[text], model=model).data[0].embedding