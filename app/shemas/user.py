from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    roles: List[str] = []



class ProfileIn(BaseModel):
    bio: str = Field('', max_length=500)
    city: str = Field('', min_length=2, max_length=100)
    country: str = Field('', min_length=2, max_length=100)


class RegisterWithProfile(UserCreate):
    profile: ProfileIn

class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bio: str = Field(..., max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    country: str = Field(..., min_length=2, max_length=100)

class UserWithProfileOut(UserOut):
    profile: ProfileOut | None = None