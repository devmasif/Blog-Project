# #id (PK)
# post_id (FK to Post)
# author_id (FK to User)
# content
# created_at

from pydantic import BaseModel
from datetime import datetime

class CommentsBase(BaseModel):
    content: str

class AddComment(CommentsBase):
    auth_id: str
    post_id: str

class CommentUpdate(CommentsBase):
    created_at: datetime

class CommentOut(CommentsBase):
    id: str
    author_id: str
    post_id: str
    created_at: datetime

