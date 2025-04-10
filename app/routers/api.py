from fastapi import APIRouter

from app.routers import v1

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(v1.reservation.router)
router.include_router(v1.table.router)
