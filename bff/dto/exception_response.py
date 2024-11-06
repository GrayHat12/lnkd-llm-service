from fastapi import status
from fastapi.responses import JSONResponse


class BaseExceptionResponse:

    def __init__(self, message: str, status_code: status):
        self.message = message
        self.status_code = status_code

    def response(self):
        return JSONResponse(
            content={"message": self.message},
            status_code=self.status_code
        )