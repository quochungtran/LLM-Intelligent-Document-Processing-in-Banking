from llama_index.readers.web import FireCrawlWebReader
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.node_parser import SentenceSplitter
import os
import logging
import time

from src.rag.document import DocumentLoader
from src.utils import setup_logging
from src.rag.vectordb import qdrant_client
from src.brain import detect_collection, get_embedding, detect_user_intent, openai_chat_complete, gen_doc_prompt
from src.utils import process_string_to_list, get_pattern
from src.rag.data_source import DATA_URL, TOPICS

from copy import copy

setup_logging()
logger = logging.getLogger(__name__)

def getDocumentLoader(url: str):
    if get_pattern(url) == "pdf":
        reader = PDFReader()
        parser = SentenceSplitter(
            paragraph_separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
        )
        return DocumentLoader(reader, parser)
    elif get_pattern(url) == "http":
        FIRE_CRAWL_API_KEY = os.environ.get("FIRE_CRAWL_API_KEY", default=None)
        reader = FireCrawlWebReader(
            api_key=FIRE_CRAWL_API_KEY,
            mode="scrape"
        )
        parser = MarkdownNodeParser()
        return DocumentLoader(reader, parser)

def load_data_from(url: str):
    document_loader = getDocumentLoader(url)
    return document_loader.to_summerized_home_loan_nodes(url, threshold=5000)

def bot_rag_answer_message(history, message):
    user_intent = detect_user_intent(history, message)
    collections = process_string_to_list(detect_collection(history, message))

    logger.info(f"User intent: {user_intent}")

    # Embedding text
    vector = get_embedding(user_intent)
    logger.info(f"Get vector: {user_intent}")

    # Search document
    top_docs = []
    for collection_name in collections:
        top_docs += qdrant_client.search_vectors(collection_name, vector, 2)
    
    logger.info(f"Top docs: {top_docs}")

    # Use history as openai messages
    openai_messages = copy(history)

    gen_doc = gen_doc_prompt(top_docs)
    # Update documents to prompt
    openai_messages.extend(
        [
            {"role": "user", "content": gen_doc},
            {"role": "user", "content": message},
        ]
    )

    logger.info(f"Openai messages: {openai_messages}")

    assistant_answer = openai_chat_complete(openai_messages)

    logger.info(f"Bot RAG reply: {assistant_answer}")
    return assistant_answer, gen_doc

def rag_flow_implementation(collection_name, urls):
    doc_objects = []
    print(f"Collection: {collection_name}")
    
    for url in urls:
        doc_objects += load_data_from(url)
    
    time.sleep(25)

    for doc in doc_objects:
        qdrant_client.add_doc(doc, collection_name)
    
def tear_down():
    for topic in TOPICS:
        qdrant_client.get_client().delete_collection(topic)

if __name__=="__main__":
    # tear_down()
    for topic in TOPICS:
        docs = rag_flow_implementation(topic, DATA_URL[topic])