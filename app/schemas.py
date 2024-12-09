from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class VideogameBase(BaseModel):
    title: str
    description: Optional[str] = None

class VideogameCreate(VideogameBase):
    pass

class VideogameUpdate(VideogameBase):
    pass

class Videogame(VideogameBase):
    id: int
    status: str

    class Config:
        from_attributes = True