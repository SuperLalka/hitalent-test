import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from src.config.settings import settings
from src.routers.api import router as router_api
from src.routers.ssr import router as router_ssr

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=settings.DEBUG,
)


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
