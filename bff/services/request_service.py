import pymongo
from fastapi import Request

from dto.request import LnkdRequestDto, LnkdResponseDto
from dao.lnkd_requests import LnkdRequestDao, RequestStatus
from services.auth_service import AuthService

from config.client_config import lnkd_request_db
from exceptions.custom_exceptions import ResourceNotFoundException

class RequestService(AuthService):

    def get_request(self, requestid: str):
        found = lnkd_request_db().find_one({
            "user_id": self._user.user_id,
            "lnkd_request_id": requestid
        })
        if not found:
            raise ResourceNotFoundException("Resource not found")
        return LnkdResponseDto.model_validate(found)

    def get_history(self, page: int = 1, limit: int = 20):
        cursor = lnkd_request_db().find({
            "user_id": self._user.user_id
        }).sort("_id", pymongo.DESCENDING)

        if limit > -1:
            cursor.skip(limit * (page - 1))
            cursor.limit(limit)
        
        return [LnkdRequestDto.model_validate(doc) for doc in cursor]

    def create_request(self, lnkd_request: LnkdRequestDto, request: Request):
        doc = LnkdRequestDao(
            tagret_profile=lnkd_request.tagret_profile,
            status_message="Queued",
            status=RequestStatus.QUEUED,
            request_id=request.state.request_id,
            user_id=self._user.user_id,
            lnkd_username=lnkd_request.lnkd_username,
            lnkd_password=lnkd_request.lnkd_password
        )
        try:
            # TODO: Push to some queue
            pass
        except:
            doc.status = RequestStatus.FAILED
            doc.status_message = "Failed to Queue"
        lnkd_request_db().insert_one(doc.model_dump(mode='python'))
        return LnkdResponseDto.model_validate(doc.model_dump(mode='python'))