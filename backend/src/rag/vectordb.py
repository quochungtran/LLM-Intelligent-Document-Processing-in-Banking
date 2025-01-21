from abc import ABC, abstractmethod
import logging

from llama_index.core.schema import TextNode
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from config import Config
from src.brain import get_embedding

logger = logging.getLogger(__name__)

class VectorDBQueryManagement(ABC):
    @abstractmethod
    def create_collection(self, name: str, vector_size: int, distance_op: str):
        """
        Create a collection in Qdrant.
        Args:
            name: Name of the collection.
            vector_size: Dimension of the vectors (default: 1536).
            distance: Distance metric for similarity search (default: "DOT").
        """
        pass

    @abstractmethod
    def add_vectors(self, collection_name: str, vectors: dict):
        """
        Add vector list to a collection.
        Args:
            collection_name: Name of the collection.
            vectors: A dictionary where keys are vector IDs, and values contain vector data and payload.
        """
        pass

    @abstractmethod
    def search_vectors(self, collection_name: str, query_vector: list, limit: int):
        """
        Search for vectors in a collection.
        Args:
            collection_name: Name of the collection.
            query_vector: The vector to use for similarity search.
            limit: Number of results to return (default: 4).
        """
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """Delete the collection."""
        pass

    @abstractmethod
    def get_client(self):
        """
        get client
        Args:
            vector_db_client
        """
        pass
    
    @abstractmethod
    def add_doc(self, node_instance: TextNode, collection_name="llm"):
        """
        add/embedding document into vector database
        Args:
            node_instance: TextNode presented chunking text
            collection_name: collection name 
        """
        pass

class QdrantQueryManagement(VectorDBQueryManagement):

    DEFAULT_VECTOR_SIZE = 1536
    DEFAULT_DISTANCE_OP = Distance.DOT

    def __init__(self, url: str):
        self.client = QdrantClient(url=url)
    
    def create_collection(self, name, vector_size=DEFAULT_VECTOR_SIZE, distance_op=DEFAULT_DISTANCE_OP):
        if not self.client.collection_exists(name):
            logger.info(f"Creating collection '{name}' with vector size {vector_size} and distance operation {distance_op}.")
            return self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance=distance_op)
            )
        
    def add_vectors(self, collection_name: str, vectors: dict):
        points = [
            PointStruct(id=k, vector=v["vector"], payload=v["payload"])
            for k, v in vectors.items()
        ]
        return self.client.upsert(collection_name=collection_name, points=points, wait=True)

    def search_vectors(self, collection_name: str, query_vector: list, limit: int = 4):
        results = self.client.search(
            collection_name=collection_name, query_vector=query_vector, limit=limit
        )
        return [x.payload for x in results]
    
    def delete_collection(self, collection_name):
        self.client.delete_collection(collection_name=collection_name)

    def add_doc(self, node_instance: TextNode, collection_name="llm"):
        node_content = node_instance.get_content()
        if node_content:
            vector = get_embedding(node_content)
            logger.info(f"Embedding {node_content} to vector")

            qdrant_client.create_collection(collection_name)
            qdrant_client.add_vectors(
                collection_name,
                {
                    node_instance.id_: {
                        "vector": vector,
                        "payload": {
                            "content": node_content
                        }
                    }
                }
            )
        else:
            logger.info("Content is null")
    
    def get_client(self):
        return self.client

qdrant_client = QdrantQueryManagement(Config.QDRANT_URL)