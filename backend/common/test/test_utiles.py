import logging
import hashlib
import unittest
from src.utiles import *

class TestUtils(unittest.TestCase):

    def test_convert_json_to_list(self):
        input_string = '["item1", "item2", "item3"]'
        expected_result = ["item1", "item2", "item3"]

        result = convert_json_to_list(input_string)
        self.assertEqual(result, expected_result)

    def test_generate_random_string(self):
        length = 16
        random_string = generate_random_string(length)
        self.assertEqual(len(random_string), length)

    def test_generate_random_string(self):
        length = 32
        random_string1 = generate_random_string(length)
        random_string2 = generate_random_string(length)
        self.assertNotEqual(random_string1, random_string2)
    
    def test_generate_request_id_hashing(self):
        request_id1 = generate_request_id(32)
        request_id2 = generate_request_id(32)
        self.assertEqual(request_id1, request_id2)