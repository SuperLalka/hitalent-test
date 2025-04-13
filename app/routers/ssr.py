import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.repository.filters.reservation import ReservationFilter
from app.routers.depends import SessionDep
from app.services.reservation import ReservationService
from app.services.table import TableService

router = APIRouter(
    prefix="/ssr"
)
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request, session: SessionDep):
    return templates.TemplateResponse("base.html", {
        "json": json,
        "request": request,
        "tables": [
            table for table
            in await TableService(session).get_all()
        ],
    })


@router.get("/tables/{table_id}", response_class=HTMLResponse)
@router.get("/tables/{table_id}/", response_class=HTMLResponse, include_in_schema=False)
async def tables_detail(
    request: Request,
    session: SessionDep,
    table_id: int,
):
    table = await TableService(session).get_by_id(table_id)
    return templates.TemplateResponse("pages/table-detail.html", {
        "request": request,
        "table": table,
        "reservations": [
            reservation.model_dump() for reservation
            in await ReservationService(session, model_filter=ReservationFilter(table_id=table.id)).get_all()
        ],
    })
