from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from models import TaskInfo
from schemas import CreateTask, UpdateTask

from core.database import get_db

class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_tasks(self, limit: int = 10, offset: int = 0) -> List[TaskInfo]:
        return self.db.query(TaskInfo).limit(limit).offset(offset).all()

    def get_by_id(self, task_id: int) -> Optional[TaskInfo]:
        return self.db.query(TaskInfo).filter(TaskInfo.task_id == task_id).first()

    def update(self, task_id: int, task: UpdateTask) -> Optional[TaskInfo]:
        task_db = self.get_by_id(task_id)
        if not task_db:
            return None

        update_data = task.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task_db, field, value)

        self.db.commit()
        self.db.refresh(task_db)
        return task_db

    def create(self, task: CreateTask) -> TaskInfo:
        task_db = TaskInfo(**task.model_dump())
        self.db.add(task_db)
        self.db.commit()
        self.db.refresh(task_db)
        return task_db

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False