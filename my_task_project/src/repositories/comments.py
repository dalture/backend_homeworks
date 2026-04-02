from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from fastapi import Depends

from src.models import CommentInfo
from src.schemas import CreateComment, UpdateComment
from src.core.database import get_db

class CommentRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_comments(self, task_id: int, limit: int = 10, offset: int = 0) -> List[CommentInfo]:
        result = await self.db.execute(select(CommentInfo).where(CommentInfo.task_id == task_id))
        comments_by_id = result.scalars().all()
        comments = comments_by_id[offset: offset + limit]
        return comments
    
    async def get_by_id(self, task_id: int, comment_id: int) -> Optional[CommentInfo]:
        result = await self.db.execute(select(CommentInfo).where(
            and_(CommentInfo.id == comment_id,
                 CommentInfo.task_id == task_id)))
        return result.scalar_one_or_none()
    
    async def create(self, comment: CreateComment) -> CommentInfo:
        comment_db = CommentInfo(**comment.model_dump())
        self.db.add(comment_db)
        await self.db.commit()
        await self.db.refresh(comment_db)
        return comment_db

    async def delete(self, comment_id: int) -> bool:
        comment_db = await self.get_by_id(comment_id)
        if comment_db:
            await self.db.delete(comment_db)
            await self.db.commit()
            return True
        return False