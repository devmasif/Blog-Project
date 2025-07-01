from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    bio: Optional[str] = None
    created_at: datetime

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

