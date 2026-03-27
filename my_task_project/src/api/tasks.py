from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from src.schemas import CreateTask, UpdateTask, GetTask, CreateComment, UpdateComment, GetComment
from src.services import TaskService, CommentService
from dependancy import check_headers


router = APIRouter(prefix= "/tasks", tags=["Tasks"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_tasks(service: TaskService = Depends()) -> List[GetTask] | None:
    get_result = service.get_all_tasks(limit=10, offset=0)
    return JSONResponse(
        jsonable_encoder(get_result))

@router.post("/", dependencies=[Depends(check_headers)],status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask, service: TaskService = Depends()) -> JSONResponse:
    add_result = service.add_task(new_task=payload)
    return JSONResponse({
        "message": "Task created",
        "task": jsonable_encoder(add_result)
        })

@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, service: TaskService = Depends()) -> JSONResponse:
    get_result = service.get_task_by_id(task_id=task_id)
    if get_result:
        return JSONResponse(
            jsonable_encoder(get_result))

@router.patch("/{task_id}", dependencies=[Depends(check_headers)], status_code=status.HTTP_200_OK)
def update_task(task_id: int, payload: UpdateTask, service: TaskService = Depends()) -> JSONResponse:
    update_result = service.update_task(task_id=task_id, payload=payload)

    return JSONResponse(
        jsonable_encoder(update_result)
    )
    
@router.delete("/{task_id}", dependencies=[Depends(check_headers)], status_code=status.HTTP_200_OK)
def delete_task(task_id: int, service: TaskService = Depends()) -> JSONResponse:
    delete_result = service.delete_task(deleting_task_id=task_id)

    if delete_result:
        return JSONResponse(
            jsonable_encoder(delete_result)
        )

@router.post("/{task_id}/comments", status_code=status.HTTP_200_OK)
def create_comment(task_id: int, payload: CreateComment, service: CommentService = Depends()) -> JSONResponse:
    add_result = service.create_comment(new_comment=payload)
    return JSONResponse({
        "message": "Comment created",
        "comment": jsonable_encoder(add_result)
        })

@router.get("/{task_id}/comments/{comment_id}", status_code=status.HTTP_200_OK)
def get_comment(task_id: int, comment_id: int, service: CommentService = Depends()) -> JSONResponse:
    get_result = service.get_comment_by_id(comment_id=comment_id)
    return JSONResponse(
            jsonable_encoder(get_result)
            )

@router.get("/{task_id}/comments", status_code=status.HTTP_200_OK)
def get_comments(task_id: int, service: CommentService = Depends()) -> JSONResponse:
    get_result = service.get_all_comments(limit=10, offset=0)
    if not get_result:
        return JSONResponse({
            "status": "error",
            "message": "No comments found"
            }, status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(
        jsonable_encoder(get_result)
        )

@router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: int, service: CommentService = Depends()) -> JSONResponse:
    delete_result = service.delete_comment(comment_id=comment_id)

    return JSONResponse({
        "message": "Comment deleted"
        })