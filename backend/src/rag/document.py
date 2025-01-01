import logging
import nest_asyncio
from src.brain import summarize_doc_home_loan
logger = logging.getLogger(__name__)

nest_asyncio.apply()

class DocumentLoader():
    def __init__(self, url, reader, parser):
        self._reader = reader
        self._parser = parser
        self._url = url
        self._documents = self.to_doc_objects()
        self._nodes     = self.to_node_objects()
        
    def to_doc_objects(self):
        self._reader.load_data(self._url)
    
    def to_node_objects(self):
        self._parser.get_nodes_from_documents(self._documents)
    
    def to_summerized_home_loan_nodes(self, threshold=5000):
        for node in self._nodes:
            doc_content = node.get_content()
            if(len(doc_content) >= threshold):
                node.set_content(summarize_doc_home_loan(doc_content))

    def get_nodes(self):
        return self._nodes

    def nodesLogging(self):
        for i, node in enumerate(self._nodes):
            print(f"""Doc Content     :{node.get_content()}""")
            print("===================================================")
