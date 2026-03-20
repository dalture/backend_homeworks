from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models import UserInfo
from schemas import BaseUser, RegistrationUser
from core.security import hash_password

from core.database import get_db

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_users(self, limit: int = 10, offset: int = 0) -> List[UserInfo]:
        return self.db.query(UserInfo).limit(limit).offset(offset).all()

    def get_by_id(self, user_id: int) -> Optional[UserInfo]:
        return self.db.query(UserInfo).filter(UserInfo.task_id == user_id).first()
    
    def get_by_email(self, user_email: str) -> Optional[UserInfo]:
        return self.db.query(UserInfo).filter(UserInfo.user_email == user_email).first()
    
    def create(self, new_user: RegistrationUser) -> UserInfo:
        user_dict = new_user.model_dump()
        user_dict["user_password_hash"] = hash_password(new_user.password)
        user_dict.pop("password")
        db_user = UserInfo(**user_dict)

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user