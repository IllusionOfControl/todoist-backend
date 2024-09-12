from typing import Optional, Any

from fastapi import HTTPException
from fastapi.security import APIKeyHeader
from starlette import requests
from starlette.status import HTTP_403_FORBIDDEN


class TodoistTokenHeader(APIKeyHeader):
    def __init__(self, raise_error: bool, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.raise_error = raise_error

    async def __call__(
            self,
            request: requests.Request,
    ) -> Optional[str] | None:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if not self.raise_error:
                return ""
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="missing authorization credentials.",
            )

        try:
            token_prefix, token = api_key.split(" ")
        except ValueError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token schema"
            )

        if token_prefix.lower() != "token":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token schema"
            )

        return token
