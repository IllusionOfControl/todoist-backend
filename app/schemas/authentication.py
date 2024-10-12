from pydantic import BaseModel, EmailStr, Field


class SignInRequest(BaseModel):
    username: str = Field(..., description="user`s username")
    password: str = Field(..., description="user`s password")


class SignInData(BaseModel):
    access_token: str = Field(..., description="jwt access token")
    # refresh_token: str


class SignUpRequest(BaseModel):
    username: str = Field(
        title="username", description="user username", min_length=3, max_length=64
    )
    email: EmailStr = Field(title="email", description="user email")
    password: str = Field(title="password", description="user password", min_length=6)
