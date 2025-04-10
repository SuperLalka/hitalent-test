from typing import List

from fastapi import APIRouter, Body, Request

from app.routers.depends import SessionDep
from app.schemas.table import TableInput, TableOutput
from app.services.table import TableService

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


@router.get("", response_model=List[TableOutput])
@router.get("/", response_model=List[TableOutput], include_in_schema=False)
async def get_tables(
    request: Request,
    session: SessionDep
):
    return await TableService(session).get_all()


@router.post("", response_model=TableOutput)
@router.post("/", response_model=TableOutput, include_in_schema=False)
async def create_table(
    request: Request,
    session: SessionDep,
    table_data: TableInput = Body(...),
):
    return await TableService(session).create(table_data)


@router.delete("/{table_id}", status_code=204)
@router.delete("/{table_id}/", status_code=204, include_in_schema=False)
async def delete_table(
    request: Request,
    session: SessionDep,
    table_id: int,
):
    return await TableService(session).delete(table_id)
