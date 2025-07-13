from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str   

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    created_at: datetime 
    # owner: UserResponse

    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: int