from fastapi import HTTPException
from enum import Enum

class ErrorCode(Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    COMMENT_NOT_FOUND = "COMMENT_NOT_FOUND"

class AppException(HTTPException):
    def __init__(
            self,
            status_code: int,
            error_code: ErrorCode,
            message: str,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code.value,
                "message": message,
            }
        )
class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.USER_NOT_FOUND,
            message=f"Пользователь с идентификатором {user_id} не найден",
        )

class TaskNotFoundException(AppException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.TASK_NOT_FOUND,
            message=f"Задача с идентификатором {task_id} не найдена",
            )
        
class CommentNotFoundException(AppException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.COMMENT_NOT_FOUND,
            message=f"Комментарий с идентификатором {comment_id} не найден",
        )
