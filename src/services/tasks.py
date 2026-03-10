# валидация того, что исполнители из списка юзеров
from schemas import CreateTask, BaseTask, UpdateTask, GetTask, TaskImportance, TaskStatus, TaskUrgency, BaseUser

tasks = []
users = [
    BaseUser(
        id=1,
        name="Darina",
        surname="Ivanova",
        email="darina.ivanova@gmail.com"
    ),
    BaseUser(
        id=2,
        name="Maxim",
        surname="Petrov",
        email="max.petrov@gmail.com"
    ),
    BaseUser(
        id=3,
        name="Anna",
        surname="Smirnova",
        email="anna.smirnova@gmail.com"
    ),
    BaseUser(
        id=4,
        name="Ivan",
        surname="Kuznetsov",
        email="ivan.kuznetsov@gmail.com"
    ),
    BaseUser(
        id=5,
        name="Elena",
        surname="Sokolova",
        email="elena.sokolova@gmail.com"
    ),
    BaseUser(
        id=6,
        name="Dmitry",
        surname="Volkov",
        email="d.volkov@gmail.com"
    ),
]

class TaskService:
    def __init__(self):
        self.task_mock_db = tasks
    
        # вывод задачи
    def get_task(self, task_id):
        for task in self.task_mock_db:
            if task.id == task_id:
                return task.model_dump()
            
        return {
            "status": "error",
            "message": "Task not found"
            }

    # добавить задачу (чек уникальности по имени+исполнителям или id)
    def add_task(self, new_task: CreateTask):
        for task in self.task_mock_db:
            if task.name.lower() == new_task.name.lower() and set(task.id_performers) == set(new_task.id_performers):
                return {
                    "status": "error",
                    "message": "Task already exists"
                }
            elif task.id == new_task.id:
                return {
                    "status": "error",
                    "message": "Task already exists"
                }
            
        task = GetTask(**new_task.model_dump())
        self.task_mock_db.append(task)
        return {
            "status": "Success",
            "message": "Task added"
        }
    
    # обновить задачу (чек логики статусов)
    def update_task(self, task_id, task_new_data: UpdateTask):
        for task in self.task_mock_db:
            if task.id == task_id:
                to_update = task_new_data.model_dump(exclude_unset=True)

                for field, value in to_update.items():
                    if field == "status" and (task.status == TaskStatus.done and value == TaskStatus.in_progress):
                        return {
                            "status": "error",
                            "message": "Task is already done"
                        }
                    elif field == "status" and (task.status not in [TaskStatus.in_progress, TaskStatus.new] and value == TaskStatus.done):
                        return {
                            "status": "error",
                            "message": "Task cannot be markd as done"
                        }
                    elif field == "id_performers":
                        for user_id in value:
                            if not any(user.id == user_id for user in users):
                                return {
                                    "status": "error",
                                    "message": f"User with ({user_id}) id not found"
                                }
                    
                    setattr(task, field, value)
                return BaseTask(**task.model_dump())

    # удалить задачу (чек на существование)
    def delete_task(self, deleting_task: int):
        for task in self.task_mock_db:
            if task.id == deleting_task:
                self.task_mock_db.remove(task)
                return {
                    "status": "success",
                    "message": "Task deleted"
                }
        return {
            "status": "error",
            "message": "Task already deleted or not found"
        }

    # вывод всех задач
    def get_all_tasks(self):
        return [GetTask(**task.model_dump()) for task in self.task_mock_db]