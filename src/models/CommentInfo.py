from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class CommentInfo(Base):
    __tablename__ = 'comment_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("user_info.user_id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("task_info.task_id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    task = relationship("TaskInfo", back_populates="comments")
