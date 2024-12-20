from src.task.calculation import add

def test_add_task():
    result = add.apply(args=(5, 7)).get()
    assert result == 12