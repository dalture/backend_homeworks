from src.api.tasks import router as tasks_router
from src.api.users import router as users_router
from src.api.auth_user import router as auth_router

__all__ = (
    tasks_router,
    users_router,
    auth_router
)