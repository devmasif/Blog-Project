from fastapi import APIRouter, Depends, HTTPException
from models.user_models import User
from util.auth import get_current_user
from db.mongo import likes_collection, posts_collection

router = APIRouter()

@router.post(
    "/posts/{post_id}/like",
    summary="Like a post",
    description="""
Allows the authenticated user to like a specific post.

- Prevents duplicate likes.
- Fails if the post doesn't exist or is already liked.
"""
)
def like_post(
    post_id: str,
    user: User = Depends(get_current_user)
):
    post = posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = {
        "post_id": post_id,
        "user_id": user.id
    }

    if likes_collection.find_one(existing_like):
        raise HTTPException(status_code=400, detail="Post already liked")

    likes_collection.insert_one(existing_like)
    return {"message": "Liked successfully"}


@router.delete(
    "/posts/{post_id}/unlike",
    summary="Unlike a post",
    description="""
Allows the authenticated user to unlike a post they've previously liked.

- Fails if the like doesn't exist.
"""
)
def unlike_post(
    post_id: str,
    user: User = Depends(get_current_user)
):
    result = likes_collection.delete_one({
        "post_id": post_id,
        "user_id": user.id
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    
    return {"message": "Unliked successfully"}


@router.get(
    "/posts/{post_id}/likes",
    summary="Get like count",
    description="Returns the number of likes on a specific post."
)
def get_like_count(post_id: str):
    count = likes_collection.count_documents({"post_id": post_id})
    return {"post_id": post_id, "like_count": count}
