from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(..., max_length =100)
    content: str
    tags: Optional[List[str]] = []
    

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None

class PostOut(PostBase):
    id: str
    slug: str
    author_name: str
    is_published: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
 








