from pydantic import BaseModel, Field
from dao.lnkd_requests import BaseLnkdRequestModel

class LnkdRequestDto(BaseModel):
    # All of these fields should have some constraints on length idealy but i don't have enough time as of now to research all of these constraints
    
    lnkd_username: str = Field(...) # should be encrypted ideally, not doing it here, considering it out of scope for the assignment
    lnkd_password: str = Field(...) # should be encrypted ideally, not doing it here, considering it out of scope for the assignment

    tagret_profile: str = Field(..., description="For a profile https://www.linkedin.com/in/grayhat, the target_profile value will be grayhat")

class LnkdResponseDto(BaseLnkdRequestModel):
    pass