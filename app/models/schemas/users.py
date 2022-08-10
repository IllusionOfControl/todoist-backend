from pydantic import BaseModel


class UserInSignup(BaseModel):
    username: str
    email: str
    password: str


class UserInSignin(BaseModel):
    username: str
    password: str


class UserInResponse(BaseModel):
    username: str
    token: str

    class Config:
        orm_mode = True
