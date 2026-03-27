from fastapi import Depends
from typing import List

from src.repositories import CommentRepository
from src.schemas import CreateComment, GetComment
from src.core.exceptions import CommentNotFoundException

class CommentService:
    def __init__(self, repository: CommentRepository = Depends(CommentRepository)):
        self.repo = repository

    def get_comment_by_id(self, comment_id: int) -> GetComment | None:
        comment_db = self.repo.get_comment_by_id(comment_id)

        if not comment_db:
            return CommentNotFoundException(comment_id=comment_id)
        
        return comment_db
    
    def create_comment(self, new_comment: CreateComment) -> GetComment:
        return self.repo.create(new_comment)
    
    def delete_comment(self, comment_id: int) -> bool:
        result = self.repo.delete(comment_id)
        
        if not result:
            return CommentNotFoundException(comment_id=comment_id)
        
        return result
    
    def get_all_comments(self, limit, offset) -> List[GetComment] | None:
        return self.repo.get_all_comments(limit, offset)