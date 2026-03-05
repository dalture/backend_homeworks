from pydantic import BaseModel, computed_field
from typing import Optional, List
from datetime import date

from schemas.tasks_types import TaskImportance, TaskUrgency, TaskStatus
from schemas.users import BaseUser

# для update
class BaseTask(BaseModel): 
    id: int
    name: str
    description: Optional[str] = None
    importance: Optional[TaskImportance] = None
    urgency: Optional[TaskUrgency] = None
    status: TaskStatus
    deadline: Optional[date] = None
    id_performers: List[BaseUser] = []

    @computed_field
    def performers_count(self) -> int:
        return len(self.id_performers)

class CreateTask(BaseTask): # для create и всего остального (нельзя менять время создания, но можно видеть, удалять, создавать его)
    creation_time: date
    id_owner: BaseUser # кто создал задачу