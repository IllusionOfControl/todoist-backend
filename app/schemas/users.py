from pydantic import BaseModel, EmailStr, Field


class UserInSignup(BaseModel):
    username: str = Field(title="username", description="user username", min_length=3, max_length=64)
    email: EmailStr = Field(title="email", description="user email")
    password: str = Field(title="password", description="user password", min_length=6)


class UserInSignin(BaseModel):
    username: str
    password: str


class UserInResponse(BaseModel):
    username: str
    token: str
