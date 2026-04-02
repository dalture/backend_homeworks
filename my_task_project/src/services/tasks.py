from fastapi import Depends, UploadFile, HTTPException
from typing import List
import uuid

from src.schemas import CreateTask, UpdateTask, GetTask, TaskStatus
from src.repositories import TaskRepository
from src.core.exceptions import TaskNotFoundException
from src.core.adapters import get_storage
from src.adapters.storage.base import StorageAdapter

class TaskService:
    def __init__(self, 
                repository: TaskRepository = Depends(TaskRepository), 
                storage: StorageAdapter = Depends(get_storage)):
        self.repo = repository
        self.storage = storage
    
        # вывод задачи
    async def get_task_by_id(self, task_id: int) -> GetTask | None:
        task_db = await self.repo.get_by_id(task_id)

        if not task_db:
            return TaskNotFoundException(task_id=task_id)
        
        return task_db

    # добавить задачу
    async def add_task(self, new_task: CreateTask) -> GetTask:        
        task_db = await self.repo.create(new_task)
        return task_db
    
    async def upload_task_avatar(self, task_id: int, image: UploadFile | None) -> str:
        task = await self.repo.get_by_id(task_id)
        if not task:
            return TaskNotFoundException(task_id=task_id)
        
        if image is not None:
            content = await image.read()
            ext = image.filename.split('.')[-1] if image.filename else "bin"
            if ext not in ("jpeg", "jpg", "png"):
                raise HTTPException(400, "Invalid image format")

            key = f"posts/{uuid.uuid4()}.{ext}"
            avatar_url = await self.storage.upload(content, key, image.content_type or "application/octet-stream")

            self.update_task(task_id=task_id, payload=UpdateTask(avatar_url=avatar_url))
            return avatar_url
        else:
            return {
                "status": "error",
                "message": "No image provided"
            }
    
    # обновить задачу (чек логики статусов)
    async def update_task(self, task_id: int, payload: UpdateTask) -> GetTask | None:
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
        task_db = await self.repo.update(task_id, payload)

        if not task_db:
            return TaskNotFoundException(task_id=task_id)
        
        return task_db

    # удалить задачу (чек на существование)
    async def delete_task(self, deleting_task_id: int) -> GetTask | None:
        task_db = await self.repo.get_by_id(deleting_task_id)

        if not task_db:
            return TaskNotFoundException(task_id=deleting_task_id)
        
        result = await self.repo.delete(deleting_task_id)
        if result:
            return {
                    "status": "success",
                    "message": "Task deleted"
            }

    # вывод всех задач
    async def get_all_tasks(self, limit, offset) -> List[GetTask] | None:
        return await self.repo.get_all_tasks(limit, offset)