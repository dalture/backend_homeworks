from fastapi import Depends
from typing import List

from src.repositories import CommentRepository
from src.schemas import CreateComment, GetComment
from src.core.exceptions import CommentNotFoundException

class CommentService:
    def __init__(self, repository: CommentRepository = Depends(CommentRepository)):
        self.repo = repository

    async def get_comment_by_id(self, task_id: int, comment_id: int) -> GetComment | None:
        comment_db = await self.repo.get_by_id(task_id, comment_id)

        if not comment_db:
            return CommentNotFoundException(comment_id=comment_id)
        
        return comment_db
    
    async def create_comment(self, new_comment: CreateComment) -> GetComment:
        return await self.repo.create(new_comment)
    
    async def delete_comment(self, comment_id: int) -> bool:
        result = await self.repo.delete(comment_id)
        
        if not result:
            return CommentNotFoundException(comment_id=comment_id)
        
        return result
    
    async def get_all_comments(self, task_id, limit, offset) -> List[GetComment] | None:
        return await self.repo.get_all_comments(task_id, limit, offset)
    
    async def get_comments_by_id(self, comment_id: int) -> GetComment | None:
        return await self.repo.get_by_id(comment_id)