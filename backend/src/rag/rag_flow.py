from llama_index.readers.web import FireCrawlWebReader
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.node_parser import SentenceSplitter

from src.rag.document import DocumentLoader
from src.utils import setup_logging
from src.rag.vectordb import qdrant_client
from src.brain import detect_collection, get_embedding, detect_user_intent, openai_chat_complete, gen_doc_prompt
from src.utils import process_string_to_list, get_pattern

import os
import logging
from copy import copy

setup_logging()
logger = logging.getLogger(__name__)

def load_url_data(url):
    document_loader = None
    if get_pattern(url) == "pdf":
        reader = PDFReader()
        parser = SentenceSplitter(
            paragraph_separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
        )
        document_loader = DocumentLoader(reader, parser)
    elif get_pattern(url) == "http":
        FIRE_CRAWL_API_KEY = os.environ.get("FIRE_CRAWL_API_KEY", default=None)
        reader = FireCrawlWebReader(
            api_key=FIRE_CRAWL_API_KEY,
            mode="crawl"
        )
        parser = MarkdownNodeParser()
        document_loader = DocumentLoader(reader, parser)

    return document_loader.to_summerized_home_loan_nodes(threshold=5000)

def add_doc_to_vector_db(node_instance, collection_name="llm"):
    if node_instance.get_content():
        vector = get_embedding(node_instance.get_content())
        logger.info(f"Embedding {node_instance.get_content()} to vector")
        qdrant_client.add_vectors(
            collection_name,
            {
                node_instance.id_: {
                    "vector": vector,
                    "payload": {
                        "content": node_instance.get_content()
                    }
                }
            }
        )
    else:
        logger.info("Title and content is null")

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

    # Update documents to prompt
    openai_messages.extend(
        [
            {"role": "user", "content": gen_doc_prompt(top_docs)},
            {"role": "user", "content": message},
        ]
    )

    logger.info(f"Openai messages: {openai_messages}")

    assistant_answer = openai_chat_complete(openai_messages)

    logger.info(f"Bot RAG reply: {assistant_answer}")
    return assistant_answer