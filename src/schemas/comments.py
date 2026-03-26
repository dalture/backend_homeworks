from pydantic import BaseModel, Field
from datetime import datetime 

class CreateComment(BaseModel):
    comment_text: str = Field(max_length=2000, min_length=1)
    owner_id: int
    task_id: int

class GetComment(BaseModel):
    owner_id: int
    comment_text: str = Field(max_length=2000, min_length=1)
    created_at: datetime

class UpdateComment(BaseModel):
    comment_text: str = Field(max_length=2000, min_length=1)