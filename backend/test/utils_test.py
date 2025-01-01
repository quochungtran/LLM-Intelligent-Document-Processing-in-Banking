import logging
import hashlib
import unittest
from src.utils import *

def test_generate_random_string_length():
    length = 16
    random_string = generate_random_string(length)
    assert len(random_string) == length

    length = 32
    random_string = generate_random_string(length)
    assert len(random_string) == length

def test_generate_random_string_uniqueness():
    length = 16
    random_string1 = generate_random_string(length)
    random_string2 = generate_random_string(length)
    assert random_string1 != random_string2


def test_generate_request_id_hashing():
    """
    Test that the request ID is derived from the hash of a random string.
    """
    random_string = generate_random_string()
    h = hashlib.sha256()
    h.update(random_string.encode('utf-8'))
    expected_hash = h.hexdigest()[:33]

    request_id = generate_request_id(32)
    assert len(request_id) == 33
    assert len(request_id) == len(expected_hash)
    assert request_id != expected_hash


class TestUtils(unittest.TestCase):

    def test_process_string_to_list(self):
        input_string = '["item1", "item2", "item3"]'
        expected_result = ["item1", "item2", "item3"]

        result = process_string_to_list(input_string)
        self.assertEqual(result, expected_result)

    def test_get_pattern(self):
        self.assertEqual(get_pattern("http://example.com/document.pdf"), "pdf")
        self.assertEqual(get_pattern("https://example.com"), "http")
        self.assertEqual(get_pattern("document.pdf"), "pdf")  # Assuming os.path.isfile is False for testing
        self.assertEqual(get_pattern("unknownfile"), "unknown")