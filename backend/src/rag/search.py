from IPython.display import Markdown, display
from llama_index.core import StorageContext, Document, SummaryIndex
from llama_index.core import StorageContext, Document, SummaryIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
import nest_asyncio
nest_asyncio.apply()
import logging

logging.basicConfig(level=logging.INFO)


class SearchDocumentEngine:
    def __init__(self, query_engine, parser_engine, rerank_engine):
        self._query_engine  = query_engine
        self._parser_engine = parser_engine
        self._rerank_engine = rerank_engine 
    
    def get_relevant_nodes(self, top_k):
        responses = self._query_engine.engine()
        return responses.source_nodes[:top_k]

    def search(self, query, top_k, num_candidates):
        """
        retrieval top num_candidates and rerank top_k
        """
        print("Input question: ", query)    
        
        relevant_nodes = self.get_relevant_nodes(query=query, top_k=num_candidates)
        relevant_chunks = self._parser_engine.parse_nodes_to_list(relevant_nodes)

        return self._rerank_engine.rerank(query=query, documents=relevant_chunks, top_n=top_k, model='rerank-multilingual-v3.0')
