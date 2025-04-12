
from typing import List

from fastapi import APIRouter, Body, Request
from pydantic import UUID4

from app.routers.depends import SessionDep
from app.schemas.reservation import ReservationInput, ReservationOutput
from app.services.reservation import ReservationService

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.get("", response_model=List[ReservationOutput])
@router.get("/", response_model=List[ReservationOutput], include_in_schema=False)
async def get_reservations(
    request: Request,
    session: SessionDep
):
    return await ReservationService(session).get_all()


@router.post("", response_model=ReservationOutput)
@router.post("/", response_model=ReservationOutput, include_in_schema=False)
async def create_reservation(
    request: Request,
    session: SessionDep,
    reservation_data: ReservationInput = Body(...),
):
    return await ReservationService(session).create(reservation_data)


@router.delete("/{reservation_id}", status_code=204)
@router.delete("/{reservation_id}/", status_code=204, include_in_schema=False)
async def delete_reservation(
    request: Request,
    session: SessionDep,
    reservation_id: UUID4,
):
    return await ReservationService(session).delete(reservation_id)
