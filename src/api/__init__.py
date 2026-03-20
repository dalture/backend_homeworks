from api.tasks import router as tasks_router
from api.users import router as users_router
from api.auth_user import router as auth_router

__all__ = (
    tasks_router,
    users_router,
    auth_router
)