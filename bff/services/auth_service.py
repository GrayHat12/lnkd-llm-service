from typing import Optional
from fastapi import Header, Request
from config.client_config import request_log_db
from common_constants.support import ID_PATTERN
from validations.token_validation import validate_token

class AuthService:
    def __init__(self, request: Request, x_api_key: Optional[str] = Header(None, pattern=ID_PATTERN, alias="x-api-key")):
        self._user = validate_token(x_api_key)

        request_log_db().update_one({
            "_id": request.state.request_log_id
        }, {
            "$set": {
                "user_id": self._user.user_id
            }
        })