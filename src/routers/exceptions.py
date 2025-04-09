import datetime

from fastapi.responses import JSONResponse


def bad_request(message_text: str = None):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 400,
        "error": "Bad Request",
        "message": message_text or "Bad Request",
    }
    return JSONResponse(status_code=400, content=response)


def unauthorized(message_text: str = None):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 401,
        "error": "Unauthorized",
        "message": message_text or "You're not authorized",
    }
    return JSONResponse(status_code=401, content=response)


def forbidden(message_text: str = None):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 403,
        "error": "Forbidden",
        "message": message_text or "You're not allowed to access",
    }
    return JSONResponse(status_code=403, content=response)


def not_found(message_text: str = None):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 404,
        "error": "Not Found",
        "message": message_text or "No object found with the specified data",
    }
    return JSONResponse(status_code=404, content=response)
