import logging
import nest_asyncio
from src.brain import summarize_doc_home_loan
logger = logging.getLogger(__name__)

nest_asyncio.apply()

class DocumentLoader():
    def __init__(self, url, reader, parser):
        self._reader = reader
        self._parser = parser
        
    def to_doc_objects(self, url):
        return self._reader.load_data(url)
    
    def to_node_objects(self, url):
        document_obj = self.to_doc_objects(url)
        return self._parser.get_nodes_from_documents(document_obj)
    
    def to_summerized_home_loan_nodes(self, url, threshold=5000):
        nodes_obj = self.to_node_objects(url)
        for node in nodes_obj:
            doc_content = node.get_content()
            if(len(doc_content) >= threshold):
                node.set_content(summarize_doc_home_loan(doc_content))
        
        return nodes_obj