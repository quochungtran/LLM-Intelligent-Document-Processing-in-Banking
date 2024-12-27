from celery import shared_task
from src.celery_app import celery_app

@shared_task()
def add(x, y):
    return x + y

@shared_task()
def multiply(x, y):
    return x * y
