from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from typing import List, Callable
from jose import JWTError, jwt
from ..core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def validate_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Validate the JWT token and return the decoded payload
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, request: Request):
        credentials = security(request)
        payload = validate_token(credentials)
        user_role = payload.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=403, detail=f"Operation not permitted for role {user_role}"
            )
        return payload


def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Decorator for endpoints that require specific roles
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise HTTPException(status_code=422, detail="Request object not found")

            checker = RoleChecker(allowed_roles)
            payload = checker(request)

            # Add user info to request state for use in endpoint
            request.state.user = payload

            return await func(*args, **kwargs)

        return wrapper

    return decorator
