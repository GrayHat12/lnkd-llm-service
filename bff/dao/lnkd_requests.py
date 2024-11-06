from typing import Optional
from utils import generate_unique_id
from common_constants.support import ID_PATTERN
from pydantic import BaseModel, Field, computed_field

from enum import IntEnum, auto

class RequestStatus(IntEnum):
    QUEUED = auto()
    RETRIEVING_POSTS = auto()
    GENERATING_WELCOME_MESSAGE = auto()
    COMPLETED = auto()
    FAILED = auto()

class Post(BaseModel):
    post_content: str = Field(...)
    hashtags: list[str] = Field([])

class BaseLnkdRequestModel(BaseModel):
    lnkd_request_id: str = Field(default_factory=generate_unique_id, description="The unique linkedin scraping and message requestid")
    tagret_profile: str = Field(...)

    target_headline: Optional[str] = Field(None)
    target_name: Optional[str] = Field(None)

    posts: Optional[list[Post]] = Field(None)
    message: Optional[str] = Field(None)
    
    status_message: str = Field(...)
    status: RequestStatus = Field(RequestStatus.QUEUED)

class LnkdRequestDao(BaseLnkdRequestModel):

    request_id: str = Field(..., pattern=ID_PATTERN, description="The api call this request is associated to. In future one api request id might be associated to multiple lnkd_request_id 's")
    user_id: str = Field(..., pattern=ID_PATTERN)
    
    # All of these fields should have some constraints on length idealy but i don't have enough time as of now to research all of these constraints
    lnkd_username: str = Field(...) # should be encrypted ideally, not doing it here, considering it out of scope for the assignment
    lnkd_password: str = Field(...) # should be encrypted ideally, not doing it here, considering it out of scope for the assignment

    @computed_field
    @property
    def linkedin_url(self) -> str:
        """
        - This will not work for cases where the user has not yet configured a custom profile url
        But I'm going to ignore those cases now. Will need more time to think about how to safely include those accounts as well
        
        - Even this implementation leaves possible vulnerabilities wherein someone can add a query or some additional flags to the linkedin profile url
        Not very safe but i don't have time to think of it as of now. Possibly a simple regex in target_profile validation should help this.
        """
        return f"https://www.linkedin.com/in/{self.tagret_profile}"