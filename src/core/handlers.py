from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Dict

from src.core.exceptions import AppException, ErrorCode

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
            headers=get_error_headers(exc.status_code)
        )   
    
def get_error_headers(status_code: int) -> Dict[str, str]:
    headers = {}

    if status_code == 401:
        headers["WWW-Authenticate"] = 'Bearer realm="api"'

    return headers