from src.rag.vectordb import QdrantQueryManagement
from src.brain import get_embedding

from llama_index.core.schema import TextNode
import unittest

class VectorDatabaseManagementTest(unittest.TestCase):
    def setUp(self):
        self.mock_collection_name = "mock_collection"
        self.mock_qdrant_client = QdrantQueryManagement(url="http://localhost:6333")
        # add different vector db here

    def tearDown(self): #note that tearDown is running at the end of each test function
        self.mock_qdrant_client.get_client().delete_collection(collection_name=self.mock_collection_name)
        
    def test_creat_collection(self):
        self.mock_qdrant_client.create_collection(self.mock_collection_name, vector_size=3)
        self.assertTrue(self.mock_qdrant_client.get_client().collection_exists(self.mock_collection_name))

    def test_search_vectors(self):
        self.mock_qdrant_client.create_collection(self.mock_collection_name, vector_size=3)
        vectors = {
            1: {"vector": [0.1, 0.2, 0.3], "payload": {"key": "value1"}},
            2: {"vector": [0.4, 0.5, 0.6], "payload": {"key": "value2"}},
            3: {"vector": [1.8, 1.9, 2],   "payload": {"key": "value3"}},
            4: {"vector": [0.9, 1.5, 1.6], "payload": {"key": "value4"}}
        }
        vector_search = [0.9, 1.5, 1.6]

        self.mock_qdrant_client.add_vectors(self.mock_collection_name, vectors)
        results = self.mock_qdrant_client.search_vectors(collection_name=self.mock_collection_name,
                                                        query_vector=vector_search,
                                                        limit=1)

        expected = [{'key': 'value3'}]
        self.assertEqual(results, expected)

    def test_add_doc(self):        
        node_instance_1 = TextNode(text="I am a good at Math")
        node_instance_2 = TextNode(text="I am a good at English")

        self.mock_qdrant_client.add_doc(node_instance_1, self.mock_collection_name)
        self.mock_qdrant_client.add_doc(node_instance_2, self.mock_collection_name)

        query = "I love Math"
        query_vector = get_embedding(query)

        expected = self.mock_qdrant_client.search_vectors(self.mock_collection_name, query_vector, limit=1)
        
        self.assertEqual(expected[0]["content"], "I am a good at Math")