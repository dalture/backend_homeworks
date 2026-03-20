from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base
from models import UserInfo

class TaskInfo(Base):
    __tablename__ = "task_info"

    task_id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(255), nullable=False)
    task_description = Column(String(255), nullable=True)
    id_owner = Column(Integer, ForeignKey("UserInfo.user_id"), nullable=False)
    importance = Column(String(16), nullable=True)
    urgency_id = Column(String(16), nullable=True)
    status_id = Column(String(16), nullable=False)
    task_created_at = Column(DateTime(timezone=True), server_default=func.now())
    task_deadline = Column(DateTime(timezone=True), nullable=True)