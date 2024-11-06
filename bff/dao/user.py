from typing import Optional
from common_constants.support import PHONE_PATTERN, ID_PATTERN
from utils import generate_unique_id
from pydantic import BaseModel, Field, EmailStr

class BaseUserModel(BaseModel):
    username: str = Field(...)
    email: Optional[EmailStr] = Field(None)
    phone: str = Field(..., min_length=10, max_length=10, pattern=PHONE_PATTERN)

class UserDao(BaseUserModel):
    api_key: Optional[str] = Field(None, pattern=ID_PATTERN)
    active: bool = Field(True)
    user_id: str = Field(default_factory=generate_unique_id, pattern=ID_PATTERN)