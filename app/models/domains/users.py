from pydantic import BaseModel, Field
from app.services import security
from datetime import datetime


class UserDomain(BaseModel):
    id: int = Field(0)
    username: str
    email: str
    password_hash: str = ""
    password_salt: str = ""
    created_at: datetime = ""
    updated_at: datetime = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.password_salt + password, self.password_hash)

    def change_password(self, password: str) -> None:
        self.password_salt = security.generate_salt()
        self.password_hash = security.get_password_hash(self.password_salt + password)
