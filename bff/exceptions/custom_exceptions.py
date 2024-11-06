from fastapi import status

class CoreException(Exception):
    pass

class ResourceNotFoundException(CoreException):
    def __init__(self, message: str, status_code: int = status.HTTP_424_FAILED_DEPENDENCY):
        self.message = message
        self.status_code = status_code

class RequestExpiredException(CoreException):
    def __init__(self, message: str, status_code: int = status.HTTP_424_FAILED_DEPENDENCY):
        self.message = message
        self.status_code = status_code

class AccessForbiddenException(CoreException):
    def __init__(self, message: str):
        self.message = message

class AccessUnauthorisedException(CoreException):
    def __init__(self, message: str):
        self.message = message

class DuplicateResourceException(CoreException):
    def __init__(self, message: str):
        self.message = message

class InvalidValueException(CoreException):
    def __init__(self, message: str):
        self.message = message

class DBOperationException(CoreException):
    def __init__(self, message: str, status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE) -> None:
        self.message = message
        self.status_code = status_code