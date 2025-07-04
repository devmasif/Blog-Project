from fastapi import APIRouter, HTTPException, Depends, status
from models.comment_models import CommentOut, CommentsBase, CommentUpdate
from models.user_models import User
from db.mongo import comments_collection, posts_collection
from util.auth import get_current_user
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter()


@router.get(
    "/posts/{post_id}/comments",
    response_model=List[CommentOut],
    summary="List comments on a post",
    description="Returns all comments for the specified post ID.",
    tags=["Comments"]
)
def list_comments_on_post(post_id: str):
    post_comments = comments_collection.find({"post_id": post_id})
    comments = []
    for comment in post_comments:
        comments.append(
            CommentOut(
                id=str(comment.get("_id")),
                post_id=comment.get("post_id", ""),
                author_id=comment.get("author_id", ""),
                content=comment.get("content", ""),
                created_at=comment.get("created_at")
            )
        )
    return comments


@router.post(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    summary="Add a comment to a post",
    description="Allows an authenticated user to comment on a specific post.",
    tags=["Comments"]
)
def add_comment(
    post_id: str,
    comments_data: CommentsBase,
    user: User = Depends(get_current_user),
):
    post = posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = {
        "content": comments_data.content,
        "author_id": user.id,
        "post_id": post_id,
        "created_at": datetime.utcnow(),
    }

    comments_collection.insert_one(new_comment)
    return {"message": "Comment added successfully"}


@router.put(
    "/comments/{id}",
    summary="Edit your comment",
    description="Allows the author to update the content of their comment.",
    tags=["Comments"]
)
def edit_comment(
    id: str,
    upd_comment: CommentUpdate,
    user: User = Depends(get_current_user)
):
    comment = comments_collection.find_one({"_id": ObjectId(id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["author_id"] != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    upd_data = upd_comment.dict(exclude_unset=True)
    comments_collection.update_one({"_id": ObjectId(id)}, {"$set": upd_data})
    return {"message": "Comment updated successfully"}


@router.delete(
    "/comments/{id}",
    summary="Delete your comment",
    description="Allows the author to delete their comment.",
    tags=["Comments"]
)
def delete_comment(
    id: str,
    user: User = Depends(get_current_user)
):
    comment = comments_collection.find_one({"_id": ObjectId(id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["author_id"] != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    comments_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Comment deleted successfully"}
