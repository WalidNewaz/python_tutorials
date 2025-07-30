import pytest
from task_manager import TaskManager

@pytest.fixture
def manager():
    return TaskManager()

def test_add_task(manager):
    task = manager.add_task("test task", "description")
    assert task is not None
    assert len(manager.tasks) == 1
    assert manager.tasks[0].name == "test task"
    assert manager.tasks[0].description == "description"
    assert manager.tasks[0].completed is False

def test_complete_task(manager):
    task = manager.add_task("test task", "description")
    manager.tasks[0].completed = True
    assert manager.tasks[0].completed is True

def test_list_tasks(manager):
    manager.add_task("test task", "description")
    manager.add_task("test task2")
    tasks = manager.list_tasks()
    assert len(tasks) == 2
    assert "[Pending] test task: description" in tasks[0]
    assert "[Pending] test task2" in tasks[1]

def test_filter_tasks(manager):
    t1 = manager.add_task("test task 1", "description")
    t2 = manager.add_task("test task 2", "description")
    t1.mark_completed()

    pending = manager.get_pending_tasks()
    completed = manager.get_completed_tasks()

    assert t2 in pending
    assert t1 in completed
