import logging
import hashlib
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
