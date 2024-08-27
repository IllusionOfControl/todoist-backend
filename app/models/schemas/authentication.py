from pydantic import BaseModel, EmailStr, Field


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    username: str
    user_id: str
    access_token: str
    refresh_token: str


class SignUpRequest(BaseModel):
    username: str = Field(title="username", description="user username", min_length=3, max_length=64)
    email: EmailStr = Field(title="email", description="user email")
    password: str = Field(title="password", description="user password", min_length=6)


class SignInResult(BaseModel):
    username: str
    user_id: str
    access_token: str
    refresh_token: str