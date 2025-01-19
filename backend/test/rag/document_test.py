from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.node_parser import SentenceSplitter
import unittest


# import local
from src.rag.document import DocumentLoader

class TestDocumentLoader(unittest.TestCase):
    def setUp(self):
        reader = WikipediaReader()
        parser = SentenceSplitter(chunk_size=100, 
                                  chunk_overlap=20)
        self.wiki_page    = "Cristiano Ronaldo"
        self.loaderEngine = DocumentLoader(reader, parser)

    def test_to_doc_objects(self):
        doc_objects = self.loaderEngine.to_doc_objects(self.wiki_page)
        self.assertEqual(len(doc_objects), 1)
        self.assertIn(f"four European Golden Shoes",
                      doc_objects[0].get_text())
    
    def test_to_node_objects(self):
        node_objects = self.loaderEngine.to_node_objects(self.wiki_page)
        self.assertEqual(len(node_objects), 212)
        
        expected_result = (
            "Widely regarded as one of the greatest players of all time, Ronaldo has won "
            "numerous individual accolades throughout his career, such as five Ballon d'Or awards, "
            "a record three UEFA Men's Player of the Year Awards, four European Golden Shoes, "
            "and was named five times the world's best player by FIFA, the most by a European player."
        )

        self.assertEqual(node_objects[1].get_content(), expected_result)

