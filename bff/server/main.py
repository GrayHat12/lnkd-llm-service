from fastapi import Depends, FastAPI, Request
from fastapi import status
from utils import generate_unique_id, validate_ulid
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from asgi_correlation_id import CorrelationIdMiddleware
from middlewares.logging_middleware import LoggingMiddleware

from dto.exception_response import BaseExceptionResponse

from controller.controller import router

from exceptions.custom_exceptions import AccessForbiddenException, AccessUnauthorisedException, \
    DuplicateResourceException, ResourceNotFoundException,  InvalidValueException, DBOperationException, \
    RequestExpiredException

from validations.token_validation import authenticate_devs

tags = []

app = FastAPI(title="Lnkd-LLM", description="LinkedIn LLM Service", openapi_tags=tags, docs_url=None, redoc_url=None, openapi_url=None)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length", "Content-Type"]
)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    update_request_header=True,
    generator=generate_unique_id,
    validator=validate_ulid,
    transformer=lambda a: a,
)

app.add_middleware(LoggingMiddleware)

app.include_router(router, prefix="/v1")

@app.get("/openapi.json", response_class=JSONResponse, include_in_schema=False)
async def get_openapi_json(username: str = Depends(authenticate_devs)):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    return JSONResponse(openapi_schema)

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def get_docs(username: str = Depends(authenticate_devs)):
    return get_swagger_ui_html(openapi_url=app.openapi_url or "/openapi.json", title=f'{app.title} - Docs')


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
async def get_redoc(username: str = Depends(authenticate_devs)):
    return get_redoc_html(openapi_url=app.openapi_url  or "/openapi.json", title=f'{app.title} - Redoc')

"""
Handle all the custom exceptions below
"""

@app.exception_handler(AccessForbiddenException)
async def access_forbidden_exception_handler(request: Request, exception: AccessForbiddenException):
    return BaseExceptionResponse(exception.message, status_code=status.HTTP_403_FORBIDDEN).response()


@app.exception_handler(AccessUnauthorisedException)
async def access_unauthorized_exception_handler(request: Request, exception: AccessUnauthorisedException):
    return BaseExceptionResponse(exception.message, status_code=status.HTTP_401_UNAUTHORIZED).response()

@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request: Request, exception: ResourceNotFoundException):
    return BaseExceptionResponse(exception.message, status_code=exception.status_code).response()

@app.exception_handler(RequestExpiredException)
async def resource_not_found_exception_handler(request: Request, exception: RequestExpiredException):
    return BaseExceptionResponse(exception.message, status_code=exception.status_code).response()


@app.exception_handler(DuplicateResourceException)
async def duplicate_resource_exception_handler(request: Request, exception: DuplicateResourceException):
    return BaseExceptionResponse(exception.message, status_code=status.HTTP_409_CONFLICT).response()


@app.exception_handler(InvalidValueException)
async def invalid_value_exception_handler(request: Request, exception: InvalidValueException):
    return BaseExceptionResponse(exception.message, status_code=status.HTTP_403_FORBIDDEN).response()

@app.exception_handler(DBOperationException)
async def db_operation_exception_handler(request: Request, exception: DBOperationException):
    return BaseExceptionResponse(exception.message, status_code=exception.status_code).response()
