# валидация того, что исполнители из списка юзеров, что важность, срочность и статус из своих списков
from schemas import CreateTask, BaseTask, TaskImportance, TaskStatus, TaskUrgency

tasks = []
users = []

class TaskService:
    def __init__(self):
        self.task_mock_db = tasks

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

        self.task_mock_db.append(new_task)
        return BaseTask(**new_task.model_dump())
    
    # обновить задачу (чек логики статусов)
    def update_task(self, task_id, task_new_data: BaseTask):
        for task in self.task_mock_db:
            if task.id == task_id:
                to_update = task_new_data.model_dump(exclude_unset=True)

                for field, value in to_update.items():
                    if field == "importance" and value not in TaskImportance.__members__.values(): 
                        return {
                            "status": "error",
                            "message": "Invalid importance value"
                        }
                    elif field == "status" and value not in TaskStatus.__members__.values():
                        return {
                            "status": "error",
                            "message": "Invalid status value"
                        }
                    elif field == "urgency" and value not in TaskUrgency.__members__.values():
                        return {
                            "status": "error",
                            "message": "Invalid urgency value"
                        }
                    elif field == "id_performers" and value not in users:
                        return {
                            "status": "error",
                            "message": "User not found"
                        }
                    
                    setattr(task, field, value)
                    return BaseTask(**task.model_dump())
            else:
                return {
                    "status": "error",
                    "message": "Task not found"
                }

    # удалить задачу (чек на существование)
    def delete_task(self, deleting_task: BaseTask):
        for task in self.task_mock_db:
            if task.id == deleting_task.id:
                return {
                    "status": "error",
                    "message": "Task already deleted"
                }
            
        self.task_mock_db.remove(deleting_task)
        return {
            "status": "success",
            "message": "Task deleted"
        }

    # вывод задачи
    def get_task(self, task_id):
        for task in self.task_mock_db:
            if task.id == task_id:
                return BaseTask(**task.model_dump())
            else:
                return {
                    "status": "error",
                    "message": "Task not found"
                }

    # вывод всех задач
    def get_all_tasks(self):
        return [BaseTask(**task.model_dump()) for task in self.task_mock_db]