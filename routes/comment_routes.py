from fastapi import APIRouter,HTTPException,Depends
from models.post_models import PostOut,PostBase,PostCreate,PostUpdate
from models.user_models import User
from models.comment_models import CommentOut,CommentsBase,AddComment,CommentUpdate
from db.mongo import comments_collection,posts_collection
from util.auth import get_current_user
from util.slugify import convert
from datetime import datetime
from bson import ObjectId,objectid

router = APIRouter()


@router.get("/posts/{post_id}/comments")
def list_comments_on_post(post_id: str):
    post_comments = comments_collection.find({"post_id": post_id})
    comments = []

    for comment in post_comments:
        comments.append(
            CommentOut(
                id = comment.get("id", ""),
                post_id=comment.get("post_id", ""),
                author_id=comment.get("author_id", ""),
                content=comment.get("content", ""),
                created_at=comment.get("created_at")
            )
        )
    return comments

    

# POST /posts/:post_id/comments → Add comment (auth required)

@router.post("/posts/{post_id}/comments")
def AddComments(
    post_id: str,
    comments_data: CommentsBase,
    user: User = Depends(get_current_user),
    ):

    post = posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404,detail="Post Not found")
    NewComment = ({
        "content": comments_data.content,
        "author_id": user.id,
        "post_id": post_id,
        "created_at": datetime.utcnow(),
    }
    )

    
    comments_collection.insert_one(NewComment)

    return ("Added Successfully")

# PUT /comments/:id → Edit your comment
@router.put("/comments/{id}")
def EditComment(
    id: str,
    upd_comment: CommentUpdate,
    user: User = Depends(get_current_user)
):
    
    comment = comments_collection.find_one({"_id": ObjectId(id)})
    if not comment:
        raise HTTPException(status_code= 404,detail="Comment Not Found")
    upd_data = upd_comment.dict()

    comments_collection.update_one({"_id": ObjectId(id)}, {"$set": upd_data})

    return "Comment Updated Successfully"

@router.delete("/comments/{id}")
def DeleteComment(
    id: str,
    user: User = Depends(get_current_user)
):
    comment = comments_collection.find_one({"_id": ObjectId(id)})
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    
    comments_collection.delete_one(comment)

    return "Comment Deleted Successfully"
    
   






