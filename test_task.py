import pytest
from task_manager import TaskManager, Task
from unittest.mock import patch

@pytest.fixture
def task_manager():
    """Создание экземпляра TaskManager для тестов"""
    return TaskManager('test_tasks.json')


def test_add_task(task_manager):
    """Тестирование добавления задачи"""
    task_manager.tasks.clear()  # Очищаем список задач перед тестом
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    assert len(task_manager.tasks) == 1


def test_view_task(task_manager):
    """Тестирование просмотра задач"""
    task_manager.tasks.clear()
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    task_manager.view_task()
    assert task_manager.tasks[0]['name'] == "Test Task"


def test_delete_task(task_manager):
    """Тестирование удаления задачи"""
    task_manager.tasks.clear()
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    task_manager.delete_task(task_manager.tasks[0]['id'])
    assert len(task_manager.tasks) == 0


def test_edit_task(task_manager):
    """Тестирование редактирования задачи"""
    task_manager.tasks.clear()
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    task_id = task_manager.tasks[0]['id']
    task_manager.edit_task(task_id, name="Updated Task")
    assert task_manager.tasks[0]['name'] == "Updated Task"


def test_search_task(task_manager):
    """Тестирование поиска задач"""
    task_manager.tasks.clear()
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    task_manager.search_task("Test Task")
    assert len(task_manager.tasks) == 1


@patch('look.TaskManager.load_tasks', return_value=[])
def unitest_add_task(mock_load, task_manager):
    """Тестирование добавления задачи"""
    task_manager.add_task("Test Task", "This is a test task", "Test", "2024-12-31", "High")
    assert len(task_manager.tasks) == 1