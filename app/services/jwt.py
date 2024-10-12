from datetime import datetime, timedelta
from typing import Dict, Protocol

import jwt
from pydantic import ValidationError

from app.models.user import User
from app.schemas.jwt import JWTMeta, JWTUser

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week


class JWTService(Protocol):
    def __init__(self, secret_key: str) -> None:
        self._secret_key = secret_key

    @staticmethod
    def create_jwt_token(
            jwt_content: Dict[str, str],
            secret_key: str,
            expires_delta: timedelta,
    ) -> str:
        to_encode = jwt_content.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
        return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

    def create_access_token_for_user(self, user_uid: str) -> str:
        return self.create_jwt_token(
            jwt_content=JWTUser(uid=user_uid).model_dump(),
            secret_key=self._secret_key,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def get_user_uid_from_token(self, token: str) -> str:
        try:
            return JWTUser(**jwt.decode(token, self._secret_key, algorithms=[ALGORITHM])).uid
        except jwt.PyJWTError as decode_error:
            raise ValueError("unable to decode JWT token") from decode_error
        except ValidationError as validation_error:
            raise ValueError("malformed payload in token") from validation_error
