from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from schemas import CreateTask, UpdateTask, GetTask
from services import TaskService
from dependancy import check_headers


router = APIRouter(prefix= "/tasks", tags=["Tasks"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_tasks(service: TaskService = Depends()) -> List[GetTask] | None:
    get_result = service.get_all_tasks()
    if not get_result:
        return JSONResponse({
            "status": "error",
            "message": "No tasks found"
            }, status.HTTP_404_NOT_FOUND)

@router.post("/", dependencies=[Depends(check_headers)],status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask, service: TaskService = Depends()) -> JSONResponse:
    add_result = service.add_task(payload)
    return JSONResponse({
        "message": "Task created",
        "task": add_result.model_dump()
        })

@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, service: TaskService = Depends()) -> JSONResponse:
    get_result = service.get_task_by_id(task_id)
    if get_result:
        return JSONResponse(
            jsonable_encoder(get_result)
        )
    else:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, payload: UpdateTask, service: TaskService = Depends()) -> JSONResponse:
    update_result = service.update_task(task_id, payload)
    if not update_result:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")
    return JSONResponse({
        jsonable_encoder(update_result)
    })
    
@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, service: TaskService = Depends()) -> JSONResponse:
    delete_result = service.delete_task(task_id)
    if not delete_result:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")
    return JSONResponse({
        "message": "Task deleted"
        })


