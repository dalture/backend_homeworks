from pydantic import BaseModel
from typing import Optional
from datetime import date

from src.schemas.tasks_types import TaskImportance, TaskUrgency, TaskStatus

class BaseTask(BaseModel): 
    task_name: str
    task_description: Optional[str] = None
    task_importance: Optional[TaskImportance] = None
    task_urgency: Optional[TaskUrgency] = None
    task_status: TaskStatus
    task_deadline: Optional[date] = None
    id_owner: int

class CreateTask(BaseModel): 
    task_name: str
    task_description: Optional[str] = None
    task_importance: Optional[TaskImportance] = None
    task_urgency: Optional[TaskUrgency] = None
    task_status: TaskStatus
    task_deadline: Optional[date] = None
    id_owner: int

class GetTask(BaseTask):
    id_owner: int
    creation_time: date

class UpdateTask(BaseModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    task_importance: Optional[TaskImportance] = None
    task_urgency: Optional[TaskUrgency] = None
    task_status: Optional[TaskStatus] = None
    task_deadline: Optional[date] = None