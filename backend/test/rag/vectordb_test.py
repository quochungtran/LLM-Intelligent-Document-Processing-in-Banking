from src.rag.vectordb import QdrantQueryManagement

mock_collection_name     = "mock_collection"
mock_db_query_managament = QdrantQueryManagement(url="http://localhost:6333")  # Replace with your Qdrant URL if different

def TearDown():
    mock_db_query_managament.get_client().delete_collection(collection_name=mock_collection_name)

def test_create_collection():
    mock_db_query_managament.create_collection(mock_collection_name, vector_size=3)
    assert mock_db_query_managament.get_client().collection_exists(collection_name="mock_collection") == True
    
def test_search_vectors():
    vectors = {
        1: {"vector": [0.1, 0.2, 0.3], "payload": {"key": "value1"}},
        2: {"vector": [0.4, 0.5, 0.6], "payload": {"key": "value2"}},
        3: {"vector": [1.8, 1.9, 2],   "payload": {"key": "value3"}},
        4: {"vector": [0.9, 1.5, 1.6], "payload": {"key": "value4"}}
    }
    vector_search = [0.9, 1.5, 1.6]

    mock_db_query_managament.add_vectors(mock_collection_name, vectors)
    results = mock_db_query_managament.search_vectors(collection_name=mock_collection_name,
                                                      query_vector=vector_search,
                                                      limit=1)

    assert results == [{'key': 'value3'}]

TearDown()
