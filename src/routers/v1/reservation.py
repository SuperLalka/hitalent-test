import uuid
from typing import List

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.reservation import ReservationInput, ReservationOutput
from src.services.reservation import ReservationService

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.get("", response_model=List[ReservationOutput])
@router.get("/", response_model=List[ReservationOutput], include_in_schema=False)
async def get_reservations(
    request: Request,
    session: Session = Depends(get_db)
):
    return await ReservationService(session).get_all()


@router.post("", response_model=ReservationOutput)
@router.post("/", response_model=ReservationOutput, include_in_schema=False)
async def create_reservation(
    request: Request,
    reservation_data: ReservationInput = Body(...),
    session: Session = Depends(get_db)
):
    return await ReservationService(session).create(reservation_data)


@router.delete("/{reservation_id}", status_code=204)
@router.delete("/{reservation_id}/", status_code=204, include_in_schema=False)
async def delete_reservation(
        request: Request,
        reservation_id: uuid.uuid4,
        session: Session = Depends(get_db)
):
    return await ReservationService(session).delete(reservation_id)
