import logging
import nest_asyncio
from llama_index.core import Document, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.readers.wikipedia import WikipediaReader

nest_asyncio.apply()

class ParserEngine:
    def __init__(self, nodes):
        _nodes = nodes
    def parse_nodes_to_list(self):
        return [node.node.get_content() for node in self._nodes]

    def parse_nodes_to_text(self):
        return "\n".join([node.node.get_content() for node in self._nodes])


class DocumentLoader:
    """
    A class for loading documents, converting them into nodes, and creating query engines.
    """
    def __init__(self, 
                 loader, 
                 pages,
                 chunk_size=512,
                 separator='.'):
        """
        Initialize the DocumentLoader.
        :param loader: An object responsible for loading data.
        :param pages: List of pages or topics to load data from.
        """
        self._loader = loader
        self._documents = loader.load_data([pages])
        self._nodes = self.to_nodes(separator=separator, chunk_size=chunk_size)

    def to_doc_objects(self):
        """
        Convert loaded documents into Document objects.
        :return: List of Document objects.
        """
        return [Document(text=doc.text) for doc in self._documents]

    def to_nodes(self, chunk_size=512, separator="."):
        """
        Convert documents into nodes based on chunk size.
        :param chunk_size: Size of chunks for splitting documents.
        :param separator: String separator to split sentences, e.g., "." or "\n".
        :return: List of nodes.
        """
        self._nodes = SentenceSplitter(separator=separator, chunk_size=chunk_size).get_nodes_from_documents(self.to_doc_objects())
        return self._nodes

    def to_summary_index(self):
        """
        Generate a SummaryIndex from nodes.
        :param chunk_size: Size of chunks for splitting documents.
        :return: SummaryIndex object.
        """
        return SummaryIndex(nodes=self._nodes)

    def generate_query_engine(self):
        """
        Generate a query engine from documents.
        :param chunk_size: Size of chunks for splitting documents.
        :return: Tuple of (SummaryIndex, QueryEngine)
        """
        index = self.to_summary_index()
        query_engine = index.as_query_engine(similarity_top_k=2)
        return index, query_engine

    def generate_parser_engine(self):
        return ParserEngine(self._nodes)



if __name__ == "__main__":
    vinfast_loader = DocumentLoader(loader=WikipediaReader(), pages=["Vinfast"])
    vinfast_index, vinfast_query_engine = vinfast_loader.generate_query_engine()
    
    print(vinfast_query_engine.query("When is Vinfast founded ?"))
    print(vinfast_query_engine.query("Who is CEO ofVinfast    ?"))
