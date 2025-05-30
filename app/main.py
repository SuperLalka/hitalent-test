import logging.config
import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError, WebSocketRequestValidationError
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app.config.logging import LOGGING
from app.config.settings import settings
from app.routers import exceptions
from app.routers.api import router as router_api
from app.routers.ssr import router as router_ssr

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI(
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=settings.DEBUG,
)

# Configure Static
os.makedirs('app/static', mode=0o777, exist_ok=True)  # TODO: tests stub, remove
app.mount("/static", StaticFiles(directory="app/static"))


@app.on_event("startup")
async def startup():
    app.include_router(router_api)
    app.include_router(router_ssr)

    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url='/ssr')


@app.on_event("shutdown")
async def shutdown():
    pass


app.add_exception_handler(RequestValidationError, exceptions.handler_for_request_validation_error)
app.add_exception_handler(WebSocketRequestValidationError, exceptions.handler_for_request_validation_error)
app.add_exception_handler(ResponseValidationError, exceptions.handler_for_response_validation_error)
