# id (PK)
# post_id (FK to Post)
# user_id (FK to User)

from pydantic import BaseModel
from datetime import datetime

class Likes(BaseModel):
    id: str
    post_id: str
    user_id: str



