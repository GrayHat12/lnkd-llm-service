from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from utils import generate_unique_id
from config.client_config import request_log_db
from asgi_correlation_id import correlation_id

class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        
        existing_correlation_id = correlation_id.get() or generate_unique_id()
        if correlation_id.get() is None:
            correlation_id.set(existing_correlation_id)
        
        request_time = datetime.now()
        request_id = generate_unique_id()

        inserted = request_log_db().insert_one({
            "request_id": request_id,
            "correlation_id": existing_correlation_id,
            "request_time": request_time,
            "response_time": None,
            "user_id": None,
            "headers": request.headers.mutablecopy(),
            "client": request.client,
            "method": request.method,
            "url": str(request.url),
            "base_url": str(request.base_url),
            "latency": None,
            "http_status": 504
        })
        request.state.request_log_id = inserted.inserted_id
        request.state.request_id = request_id
        
        response = await call_next(request)

        response_time = datetime.now()

        request_log_db().update_one({
            "_id": inserted.inserted_id
        }, {
            "$set": {
                "response_time": response_time,
                "latency": (response_time - request_time).microseconds,
                "http_status": response.status_code
            }
        })

        return response