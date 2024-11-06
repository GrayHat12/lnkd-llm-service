import os
import secrets
import traceback

from config.logger import logger
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from exceptions.custom_exceptions import AccessUnauthorisedException, CoreException, DBOperationException

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dao.user import UserDao

from config.client_config import user_db

security = HTTPBasic()

def authenticate_devs(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    possible_user_creds = [cred.split(':') for cred in os.environ["dev_creds"].split(',')]
    for (username, password) in possible_user_creds:
        if secrets.compare_digest(credentials.username, username) and secrets.compare_digest(credentials.password, password):
            logger.info(f'Accessing dev endpoints for {credentials.username}')
            return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

def validate_token(token: Optional[str]):
    """
    middleware to verify auth token
    args:
        token: received as header param. Contains a hex encoded auth token
    raises:
        401 : Unauthorized when token is not matched.
    """
    if not token or not isinstance(token, str):
        raise AccessUnauthorisedException("Unauthorised")
    try:
        token_details = user_db().find_one({
            "api_key": token,
            "active": True
        })
        if token_details is None:
            raise AccessUnauthorisedException("Unauthorised")
        return UserDao.model_validate(token_details)
    except CoreException as e:
        raise e
    except Exception as e:
        logger.error(traceback.format_exc())
        raise DBOperationException(message="Unexpected error occured. Please try later")