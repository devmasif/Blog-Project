from fastapi import APIRouter,Depends,HTTPException
from models.like_models import Likes
from models.user_models import User
from util.auth import get_current_user
from db.mongo import likes_collection,posts_collection

router = APIRouter()


@router.post("/posts/{post_id}/like")
def LikePost(
    post_id: str,
    user: User = Depends(get_current_user)
):
    post = posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    
    existing_like = ({
        "post_id": post_id,
        "user_id": user.id
    })

    if likes_collection.find_one(existing_like):
        raise HTTPException(status_code=400, detail="Post already liked")

    Likes = {
        "post_id": post_id,
        "user_id": user.id,
    }

    likes_collection.insert_one(Likes)

    return "Liked Successfully"

# /posts/:post_id/unlike
@router.delete("/posts/{post_id}/unlike")
def Unlike(
    post_id: str,
    user: User = Depends(get_current_user)
):
    delete = likes_collection.delete_one({
        "post_id": post_id,
        "user_id": user.id
    })

    if delete.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    return "Unliked successfully"


# GET /posts/:post_id/likes → Count or list of likes
@router.get("/posts/{post_id}/likes")
def LikeCount(
    post_id: str
):
    likes = likes_collection.find({"post_id": post_id})

    count = likes_collection.count_documents({"post_id": post_id})

    return {"count": count}

