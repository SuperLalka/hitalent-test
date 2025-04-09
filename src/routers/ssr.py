import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.repository.reservation import ReservationRepository
from src.repository.table import TableRepository

router = APIRouter(
    prefix="/ssr"
)
templates = Jinja2Templates(directory="src/templates")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "json": json,
        "request": request,
    })


@router.get("/tables", response_class=HTMLResponse)
@router.get("/tables/", response_class=HTMLResponse, include_in_schema=False)
async def tables(
    request: Request,
    session: Session = Depends(get_db),
):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "tables": [
            user.model_dump_json() for user
            in await TableRepository(session).get_all()
        ],
    })


@router.get("/reservations", response_class=HTMLResponse)
@router.get("/reservations/", response_class=HTMLResponse, include_in_schema=False)
async def attachments(
    request: Request,
    session: Session = Depends(get_db),
):
    return templates.TemplateResponse("files.html", {
        "request": request,
        "reservations": [
            attach.model_dump_json() for attach
            in await ReservationRepository(session).get_all()
        ],
    })
