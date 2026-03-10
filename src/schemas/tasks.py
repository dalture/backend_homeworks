from pydantic import BaseModel, computed_field
from typing import Optional, List
from datetime import date

from schemas.tasks_types import TaskImportance, TaskUrgency, TaskStatus

class BaseTask(BaseModel): 
    id: int
    name: str
    description: Optional[str] = None
    importance: Optional[TaskImportance] = None
    urgency: Optional[TaskUrgency] = None
    status: TaskStatus
    deadline: Optional[date] = None
    id_performers: List[int] = []

    @computed_field
    def performers_count(self) -> int:
        return len(self.id_performers)

class CreateTask(BaseTask): 
    id_owner: int # кто создал задачу
    creation_time: date # когда создали задачу (по идее, должно создаваться само)

class GetTask(BaseTask):
    id_owner: int
    creation_time: date

class UpdateTask(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    importance: Optional[TaskImportance] = None
    urgency: Optional[TaskUrgency] = None
    status: Optional[TaskStatus] = None
    deadline: Optional[date] = None
    id_performers: List[int] = []