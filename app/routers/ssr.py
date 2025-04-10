import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.repository.reservation import ReservationRepository
from app.repository.table import TableRepository
from app.routers.depends import SessionDep

router = APIRouter(
    prefix="/ssr"
)
templates = Jinja2Templates(directory="app/templates")


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
    session: SessionDep
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
    session: SessionDep
):
    return templates.TemplateResponse("files.html", {
        "request": request,
        "reservations": [
            attach.model_dump_json() for attach
            in await ReservationRepository(session).get_all()
        ],
    })
