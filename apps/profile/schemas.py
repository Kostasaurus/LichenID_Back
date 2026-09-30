from pydantic import BaseModel, EmailStr, Field


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)