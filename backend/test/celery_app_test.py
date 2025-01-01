from src.celery_app import celery_app
from celery.result import AsyncResult
from src.task.calculation_task import add
from src.task.routing_task import llm_handle_message
import time

def test_celery_app_init():
    assert celery_app is not None
    assert celery_app.conf.broker_url     == "redis://localhost:6379"
    assert celery_app.conf.result_backend == "redis://localhost:6379"

def test_task_discovery():
    """
    Test that Celery auto-discovers tasks from the task, rag, and agents modules.
    """
    tasks = celery_app.tasks.keys()

    # Check that tasks from all submodules are discovered
    assert "src.task.calculation_task.add" in tasks
    assert "src.task.calculation_task.multiply" in tasks

def test_add_task():
    
    task = add.delay(5, 7)
    assert task.id is not None
    
    timeout = 10  # Maximum time to wait in seconds
    start_time = time.time()
    
    while True:
        task_result = AsyncResult(task.id)
        if task_result.status == "SUCCESS":
            assert task_result.result == 12
            break
         
        if time.time() - start_time > timeout:
            assert False, f"Task did not complete within {timeout} seconds"
        
        time.sleep(0.5) 

def test_llm_handle_message_task():
    
    task = llm_handle_message.delay("bot_123", "user_456", "Hi")
    assert task.id is not None
    
    timeout = 60  # Maximum time to wait in seconds
    start_time = time.time()
    
    while True:
        task_result = AsyncResult(task.id)
        if task_result.status == "SUCCESS":
            break
         
        if time.time() - start_time > timeout:
            assert False, f"Task did not complete within {timeout} seconds"
        
        time.sleep(0.5) 
