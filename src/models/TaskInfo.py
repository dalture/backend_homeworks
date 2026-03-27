from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.core.database import Base

class TaskInfo(Base):
    __tablename__ = "task_info"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False)
    task_description = Column(String(255), nullable=True)
    id_owner = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    task_importance = Column(String(16), nullable=True)
    task_urgency = Column(String(16), nullable=True)
    task_status = Column(String(16), nullable=False)
    task_created_at = Column(DateTime(timezone=True), server_default=func.now())
    task_deadline = Column(DateTime(timezone=True), nullable=True)

    comments = relationship("CommentInfo", back_populates="task")