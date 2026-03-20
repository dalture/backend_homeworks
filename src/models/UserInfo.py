from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base
from models import TaskInfo

class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    user_surname = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_password_hash = Column(String(255), nullable=False)
    user_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)