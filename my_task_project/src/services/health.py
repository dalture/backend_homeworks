from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette.concurrency import run_in_threadpool

from src.core.database import get_db
from src.adapters.storage.base import StorageAdapter
from src.core.adapters import get_storage
from src.core.config import settings

class SystemService:
    async def db_health_check(self, db: AsyncSession = Depends(get_db)):
        await db.execute(text("SELECT 1"))
        return "healthy"

    async def s3_health_check(self):
        session = await get_storage()
        async with session.client() as s3:
            await s3.list_buckets()
        return "healthy"

    async def get_health(self, db: AsyncSession) -> dict:
        checks = {}

        try:
            checks["database"] = await self.check_database(db)
        except Exception:
            checks["database"] = "error"

        try:
            checks["storage"] = await self.check_storage()
        except Exception:
            checks["storage"] = "error"

        overall_status = "ok"
        if "error" in checks.values():
            overall_status = "degraded"

        return {
            "status": overall_status,
            "checks": checks,
        }

    def get_info(self) -> dict:
        return {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }