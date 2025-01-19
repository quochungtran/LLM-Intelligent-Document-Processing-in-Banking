import logging
import nest_asyncio
from llama_index.core import Document
from llama_index.core.schema import TextNode
from typing import Any, List

# local import
from src.brain import summarize_doc_home_loan

logger = logging.getLogger(__name__)
nest_asyncio.apply()

class DocumentLoader():
    """
    Reponsible for loading and parser and document summerizing if
    Attributes:
        _reader: An object responsible for reading and loading data from a given URL.
        _parser: An object responsible for parsing documents into structured nodes.
    
    """
    def __init__(self, reader: Any, parser: Any) -> None:
        self._reader = reader
        self._parser = parser
        
    def to_doc_objects(self, url: str) -> List[Document]:
        if self._reader.class_name() == 'WikipediaReader':
            return self._reader.load_data(pages=[url])
        
        return self._reader.load_data(url)
    
    def to_node_objects(self, url : str) -> List[TextNode]:
        document_obj = self.to_doc_objects(url)
        return self._parser.get_nodes_from_documents(document_obj)

    def to_summerized_home_loan_nodes(self, url: str, threshold=5000) -> List[TextNode]:
        nodes_obj = self.to_node_objects(url)
        for node in nodes_obj:
            doc_content = node.get_content()
            if(len(doc_content) >= threshold):
                node.set_content(summarize_doc_home_loan(doc_content))
        
        return nodes_obj
    
    def get_parser_engine(self):
        return self._parser

    def get_reader_engine(self):
        return self._reader
