from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TaskInfo
from src.schemas import CreateTask, UpdateTask
from src.core.database import get_db

class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_tasks(self, limit: int = 10, offset: int = 0) -> List[TaskInfo]:
        result = await self.db.execute(select(TaskInfo))
        tasks_get = result.scalars().all()
        tasks = tasks_get[offset: offset + limit]
        return tasks

    async def get_by_id(self, task_id: int) -> Optional[TaskInfo]:
        result = await self.db.execute(select(TaskInfo).where(TaskInfo.task_id == task_id))
        return result.scalar_one_or_none()

    async def update(self, task_id: int, task: UpdateTask) -> Optional[TaskInfo]:
        task_db = await self.get_by_id(task_id)
        if not task_db:
            return None

        update_data = task.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task_db, field, value)

        await self.db.commit()
        await self.db.refresh(task_db)
        return task_db

    async def create(self, task: CreateTask) -> TaskInfo:
        task_db = TaskInfo(**task.model_dump())
        self.db.add(task_db)
        await self.db.commit()
        await self.db.refresh(task_db)
        return task_db

    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
            return True
        return False