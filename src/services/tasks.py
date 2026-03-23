from fastapi import Depends
from typing import List
from schemas import CreateTask, UpdateTask, GetTask, TaskStatus
from repositories import TaskRepository
from services.users import UserService

class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repo = repository
    
        # вывод задачи
    def get_task_by_id(self, task_id: int) -> GetTask | None:
        task_db = self.repo.get_by_id(task_id)
        return task_db

    # добавить задачу
    def add_task(self, new_task: CreateTask) -> GetTask | None:
        task_db = self.repo.create(new_task)
        return task_db
    
    # обновить задачу (чек логики статусов)
    def update_task(self, task_id: int, payload: UpdateTask) -> GetTask | None:
        update_info = payload.model_dump(exclude_unset=True)
        for field, value in update_info.items():
            if field == "status" and (payload.task_status == TaskStatus.done and value == TaskStatus.in_progress):
                return {
                        "status": "error",
                        "message": "Task is already done"
                        }
            elif field == "status" and (payload.task_status not in [TaskStatus.in_progress, TaskStatus.new] and value == TaskStatus.done):
                return {
                        "status": "error",
                        "message": "Task cannot be marked as done"
                        }                        
        task_db = self.repo.update(task_id, payload)
        return task_db

    # удалить задачу (чек на существование)
    def delete_task(self, deleting_task_id: int) -> bool:
        task_db = self.repo.get_by_id(deleting_task_id)
        return self.repo.delete(deleting_task_id)

    # вывод всех задач
    def get_all_tasks(self, limit, offset) -> List[GetTask] | None:
        return self.repo.get_all_tasks(limit, offset)