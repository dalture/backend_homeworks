from src.services import TaskService
from src.schemas import CreateTask
from src.models import UserInfo, TaskInfo
from src.repositories import TaskRepository

def test_create_task(get_test_db):
    test_user = UserInfo(
        user_name="test name",
        user_surname="test surname",
        user_email="test email",
        user_password_hash="test password"
    )

    get_test_db.add(test_user)
    get_test_db.commit()
    get_test_db.refresh(test_user)

    repository = TaskRepository(db=get_test_db)
    service = TaskService(repository=repository)

    payload = CreateTask(
        task_name="Task 1",
        task_status='new',
        id_owner=test_user.user_id
    )

    result = service.add_task(payload)

    assert result is not None
    assert result.task_name == "Task 1"
    assert result.task_status == 'new'
    assert result.id_owner == test_user.user_id

    test_task = get_test_db.query(TaskInfo).filter(TaskInfo.task_id == result.task_id).first()
    
    assert test_task is not None
    assert test_task.task_name == "Task 1"
    assert test_task.task_status == 'new'
    assert test_task.id_owner == test_user.user_id
