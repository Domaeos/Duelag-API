from fastapi import FastAPI, Request
from utils import logger

def add_request_id_middleware(app: FastAPI, prefix: str):
    @app.middleware("http")
    async def middleware(request: Request, call_next):
        if request.url.path.startswith(prefix):
            request_id = request.headers.get('X-Request-ID', '')
            logger.info(f"Request ID received: {request_id}")
            response = await call_next(request)
            response.headers['X-Request-ID'] = request_id
            return response
        return await call_next(request)