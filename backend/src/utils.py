import hashlib
import logging.config
import secrets
import os
import json

def setup_logging():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "default",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "INFO",
            },
        },
    })


def generate_random_string(length=16):
    """
    Generates a random string of the specified length.
    """
    return secrets.token_hex(length // 2)  # Convert to bytes


def generate_request_id(max_length=32):
    """
    Generates a random string and hashes it using SHA-256.
    """
    random_string = generate_random_string()
    h = hashlib.sha256()
    h.update(random_string.encode('utf-8'))
    return h.hexdigest()[:max_length+1]

def process_string_to_list(input_string):
    return json.loads(input_string)

def get_pattern(url):
    """
    Determines the type of resource based on the URL.
    """
    if url.endswith(".pdf") or "pdf" in url:
        return "pdf"
    elif url.startswith("http://") or url.startswith("https://"):
        return "http"
    elif os.path.isfile(url):
        # Handles local file paths
        if url.endswith(".pdf"):
            return "pdf"
        else:
            return "unknown"
    else:
        return "unknown"
    
def is_valid_json(input):
    try:
        # Try to serialize and deserialize the variable
        json.loads(json.dumps(input))
        return True
    except (TypeError, ValueError):
        return False
    