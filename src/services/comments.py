from fastapi import Depends
from typing import List

from repositories import CommentRepository
from schemas import CreateComment, UpdateComment, GetComment

class CommentService:
    def __init__(self, repository: CommentRepository = Depends(CommentRepository)):
        self.repo = repository

    def get_comment_by_id(self, comment_id: int) -> GetComment | None:
        return self.repo.get_comment_by_id(comment_id)
    
    def create_comment(self, new_comment: CreateComment) -> GetComment:
        return self.repo.create(new_comment)
    
    def delete_comment(self, comment_id: int) -> bool:
        return self.repo.delete(comment_id)
    
    def get_all_comments(self, limit, offset) -> List[GetComment] | None:
        return self.repo.get_all_comments(limit, offset)