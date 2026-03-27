from unittest.mock import MagicMock

from src.services.tasks import TaskService
from src.schemas.tasks import CreateTask

def test_create_task():
    mock_repository = MagicMock()
    mock_task = MagicMock()
    mock_task.task_name = "Task 1"
    mock_task.task_status = "new"
    mock_task.id_owner = 1

    mock_repository.create.return_value = mock_task

    service = TaskService(repository=mock_repository)

    payload = CreateTask(
        task_name="Task 1",
        task_status='new',
        id_owner=1
    )

    result = service.add_task(payload)

    assert result.task_name == "Task 1"
    assert result.task_status == 'new'
    assert result.id_owner == 1

    mock_repository.create.assert_called_once_with(payload)
