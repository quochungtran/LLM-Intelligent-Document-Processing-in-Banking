from src.rag.rag_flow import *
from src.rag.vectordb import qdrant_client

import unittest

class RagFlowTest(unittest.TestCase):
    def setUp(self):
        self._http_url   = "https://www.lendingtree.com/home/mortgage/minimum-mortgage-requirements/"
        self._collection = "eligibility" 
        self._history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]
        
    def tearDown(self):
        qdrant_client.delete_collection(self._collection)
        return 

    def test_getDocumentLoader(self):
        loader = getDocumentLoader(self._http_url) 
        self.assertEqual(loader.get_reader_engine().class_name(), "Firecrawl_reader")

    def test_full_rag_flow_implementation(self):
        rag_flow_implementation("eligibility", [self._http_url])
        self.assertTrue(qdrant_client.get_client().collection_exists(self._collection), True)

        question = "What are FHA mortgage requirements ?"
        rag_response, _ = bot_rag_answer_message(self._history, question)

        self.assertGreater(len(rag_response), 0)

