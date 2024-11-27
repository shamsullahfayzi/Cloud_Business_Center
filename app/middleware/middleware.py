from functools import wraps
from typing import List
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from ..core.security import SECRET_KEY, ALGORITHM


def validate_cookie_token(request: Request):
    print(request)
    print(request.cookies)
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No token")

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_roles(allowed_roles: List[int]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = next(
                (arg for arg in args if isinstance(arg, Request)), kwargs.get("request")
            )

            payload = validate_cookie_token(request)
            if payload.get("role") not in allowed_roles:
                raise HTTPException(status_code=403, detail="Unauthorized")

            request.state.user = payload
            return await func(*args, **kwargs)

        return wrapper

    return decorator
