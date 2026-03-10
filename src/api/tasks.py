from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from schemas import CreateTask, UpdateTask
from services import TaskService


router = APIRouter(prefix= "/tasks", tags=["Tasks"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_tasks(service: TaskService = Depends()):
    return service.get_all_tasks()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, service: TaskService = Depends()):
    add_result = service.add_task(task)
    return {
        "message": "Task created",
        "task": add_result
        }

@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, service: TaskService = Depends()):
    get_result = service.get_task(task_id)
    if not get_result:
        return JSONResponse({
            "status": "error",
            "message": "Task not found"
        }, status.HTTP_404_NOT_FOUND)

    return get_result

@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, new_task_data: UpdateTask, service: TaskService = Depends()):
    update_result = service.update_task(task_id, new_task_data)
    if not update_result:
        return JSONResponse({
            "status": "error",
            "message": "Task not found"
            }, status.HTTP_404_NOT_FOUND)
    return {
        "status": "success",
        "task": update_result
    }
    
@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, service: TaskService = Depends()):
    delete_result = service.delete_task(task_id)
    if not delete_result:
        return JSONResponse({
            "status": "error",
            "message": "Task not found"
            }, status.HTTP_404_NOT_FOUND)
    return delete_result

