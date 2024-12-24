from openai import OpenAI
from redis import InvalidResponse
import logging
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