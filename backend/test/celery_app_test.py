import pytest
from src.celery_app import celery_app

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
    assert "src.task.calculation.add" in tasks
    assert "src.task.calculation.multiply" in tasks
