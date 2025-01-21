from src.rag.vectordb import QdrantQueryManagement
import unittest

mock_collection_name     = "mock_collection"
mock_db_query_managament = QdrantQueryManagement(url="http://localhost:6333")  # Replace with your Qdrant URL if different

class VectorDatabaseManagementTest(unittest.TestCase):
    def setUp(self):
        self.mock_collection_name = "mock_collection"
        self.mock_qdrant_client = QdrantQueryManagement(url="http://localhost:6333")
        # add different vector db here

    def tearDown(self): #note that tearDown is running at the end of each test function
        self.mock_qdrant_client.get_client().delete_collection(collection_name=mock_collection_name)
        
    def test_creat_collection(self):
        self.mock_qdrant_client.create_collection(mock_collection_name, vector_size=3)
        self.assertTrue(self.mock_qdrant_client.get_client().collection_exists(self.mock_collection_name))

    def test_search_vectors(self):
        self.mock_qdrant_client.create_collection(mock_collection_name, vector_size=3)
        vectors = {
            1: {"vector": [0.1, 0.2, 0.3], "payload": {"key": "value1"}},
            2: {"vector": [0.4, 0.5, 0.6], "payload": {"key": "value2"}},
            3: {"vector": [1.8, 1.9, 2],   "payload": {"key": "value3"}},
            4: {"vector": [0.9, 1.5, 1.6], "payload": {"key": "value4"}}
        }
        vector_search = [0.9, 1.5, 1.6]

        self.mock_qdrant_client.add_vectors(mock_collection_name, vectors)
        results = self.mock_qdrant_client.search_vectors(collection_name=self.mock_collection_name,
                                                        query_vector=vector_search,
                                                        limit=1)

        expected = [{'key': 'value3'}]
        self.assertEqual(results, expected)