from common_constants.support import ID_PATTERN
from fastapi import APIRouter, status, Path, Depends, Query, Request
from services.request_service import RequestService
from dto.request import LnkdResponseDto, LnkdRequestDto

tags = [
    {
        "name": "Request History",
        "description": ""
    }
]

router = APIRouter(tags=["Request History"])

@router.get("/history", status_code=status.HTTP_200_OK, response_model=list[LnkdResponseDto])
def get_history(page: int = Query(1, ge=1), limit: int = Query(20, gt=0, lt=50), service: RequestService = Depends(RequestService)):
    return service.get_history(page, limit)

@router.get("/request/{requestid}", status_code=status.HTTP_200_OK, response_model=LnkdResponseDto)
def get_request(requestid: str = Path(..., pattern=ID_PATTERN), service: RequestService = Depends(RequestService)):
    return service.get_request(requestid)

@router.post("/request", status_code=status.HTTP_200_OK, response_model=LnkdResponseDto)
def create_request(lnkd_request: LnkdRequestDto, request: Request, service: RequestService = Depends(RequestService)):
    return service.create_request(lnkd_request, request)