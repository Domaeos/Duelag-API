from fastapi import HTTPException
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import decodeJWT, logger

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        auth: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if auth:
            if not auth.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(auth.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return auth.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            return payload is not None
        except Exception as e:
            return False

jwt_bearer = JWTBearer()