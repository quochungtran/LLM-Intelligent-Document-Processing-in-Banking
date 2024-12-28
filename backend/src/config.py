import os

class Config:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None)
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")        
    
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    CELERY_BROKER_URL     = os.getenv("CELERY_BROKER_URL",     "redis://localhost:6379")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "root_password")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "0.0.0.0")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3308")

    XGBOOST_MODEL_PATH=os.getenv("XGBOOST_MODEL_PATH")