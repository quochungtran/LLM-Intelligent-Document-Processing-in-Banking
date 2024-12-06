import cohere
from typing import List
from rerank import AbstractRerankEngine
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.response.pprint_utils import pprint_response

# Initialize Cohere client with your API key
API_KEY = "bajPfjCzRPrWxuvClu33mq0kR8mSxb2CKgdqe3Ay"
co = cohere.Client(API_KEY)


class RerankCohere(AbstractRerankEngine):
    @staticmethod
    def rerank(query: str, docs: List[str]):
        """
        Reranks a list of documents based on their relevance to the query.

        Args:
            query (str): The query string to rank documents against.
            docs (List[str]): A list of documents to be reranked.

        Returns:
            dict: The reranked results from Cohere.
        """
        return co.rerank(query=query, documents=docs)

if __name__ == "__main__":
    query = "What is the capital of France?"
    documents = [
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
        "Madrid is the capital of Spain."
    ]
    
    reranker = RerankCohere()
    # cohere_rerank = CohereRerank(api_key=API_KEY, top_n=3)

    results = reranker.rerank(query, documents)
    
    for item in results.results:
        print(f"Document Rank: {item.index}")
        print(f"Document: {documents[item.index]}")
        print(f"Relevance Score: {item.relevance_score:.5f}")
        print("\n")
