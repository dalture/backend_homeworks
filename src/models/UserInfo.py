from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    user_surname = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_password_hash = Column(String(255), nullable=False)
    user_created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)