## Pydantic models which is also schemas 

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint



class Post(BaseModel): ## This is the schema for the request body
# BaseModel is a base class for creating Pydantic models
    title: str
    content: str
    published: bool= True
    
# class CreatePost(BaseModel):
#     title: set
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool
    

class PostBase(BaseModel):
    title: str
    content: str
    published: bool =  True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
      

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 
    

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

