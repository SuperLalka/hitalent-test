from typing import List

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.table import TableInput, TableOutput
from src.services.table import TableService

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


@router.get("/", response_model=List[TableOutput])
@router.get("/", response_model=List[TableOutput], include_in_schema=False)
async def get_tables(
    request: Request,
    session: Session = Depends(get_db)
):
    return await TableService(session).get_all()


@router.post("", response_model=TableOutput)
@router.post("/", response_model=TableOutput, include_in_schema=False)
async def create_table(
    request: Request,
    table_data: TableInput = Body(...),
    session: Session = Depends(get_db)
):
    return await TableService(session).create(table_data)


@router.delete("/{table_id}", status_code=204)
@router.delete("/{table_id}/", status_code=204, include_in_schema=False)
async def delete_table(
        request: Request,
        table_id: int,
        session: Session = Depends(get_db)
):
    return await TableService(session).delete(table_id)
