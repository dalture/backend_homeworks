from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Depends

from src.models import CommentInfo
from src.schemas import CreateComment, UpdateComment
from src.core.database import get_db

class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_comments(self, limit: int = 10, offset: int = 0) -> List[CommentInfo]:
        return self.db.query(CommentInfo).limit(limit).offset(offset).all()
    
    def get_by_id(self, comment_id: int) -> Optional[CommentInfo]:
        return self.db.query(CommentInfo).filter(CommentInfo.id == comment_id).first()
    
    def create(self, comment: CreateComment) -> CommentInfo:
        comment_db = CommentInfo(**comment.model_dump())
        self.db.add(comment_db)
        self.db.commit()
        self.db.refresh(comment_db)
        return comment_db

    def delete(self, comment_id: int) -> bool:
        comment_db = self.get_by_id(comment_id)
        if comment_db:
            self.db.delete(comment_db)
            self.db.commit()
            return True
        return False