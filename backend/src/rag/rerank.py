from abc import ABC, abstractmethod
from typing import List
import cohere
from pprint import pprint

rerankResponses = {"sourceNode_id", 
                   "score", 
                   "text"
                }

class AbstractRerankEngine(ABC):
    """
    Abstract base class for reranking functionality.
    Subclasses must implement the `rerank` method.
    """

    @abstractmethod
    def rerank(self, query: str, docs: List[str]):
        """
        Reranks a list of documents based on their relevance to the query.

        Args:
            query (str): The query string to rank documents against.
            docs (List[str]): A list of documents to be reranked.

        Returns:
            Any: Reranked results (implementation-specific).
        """
        pass
