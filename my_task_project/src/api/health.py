from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.services.health import SystemService

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/health")
async def health(db: AsyncSession = Depends(get_db), service: SystemService = Depends()):
    result = await service.get_health(db)

    if result["status"] == "degraded":
        return JSONResponse(
            status_code=503,
            content=result,
        )
    else:
        return JSONResponse(
            status_code=200,
            content=result,
        )

@router.get("/info")
async def info(service: SystemService = Depends()):
    return service.get_info()