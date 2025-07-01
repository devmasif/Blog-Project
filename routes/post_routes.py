from fastapi import APIRouter,HTTPException,Depends,Query
from models.post_models import PostBase,PostCreate,PostOut,PostUpdate
from util.slugify import slugify_title,convert
from db.mongo import posts_collection
from typing import List,Optional,Any
from models.user_models import User
from util.auth import get_current_user
from datetime import datetime


router = APIRouter()

@router.get("/posts", response_model=List[PostOut])
def list_published_posts(
    author: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query: dict[str,Any] = {"is_published": True}

    if author:
        query["author_name"] = author

    if tag:
        query["tags"] = tag  

    skip = (page - 1) * limit

    cursor = posts_collection.find(query).skip(skip).limit(limit)

    posts = [convert_post(post) for post in cursor]

    return posts

#   GET /posts/:slug → View a specific post (public)

@router.get("/posts/{slug}")
def getPost(slug: str):
    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug, "is_published": True})
    if not post:
        raise HTTPException(status_code=404, detail= "Post Not found")
    
    return convert_post(post)

@router.post("/posts")
def CreatePost(
    post: PostCreate,
    current_user: User = Depends(get_current_user)         
):
    slug = slugify_title(post.title)
    post_data = post.dict()
    post_data.update({
        "slug": slug,
        "author_name": str(current_user.id),
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "is_published": True 
    })

    posts_collection.insert_one(post_data)

    return convert_post(post_data)


@router.put("/posts/{slug}")
def EditPost(
    slug: str,
    post_upd: PostUpdate,
    current_user: User = Depends(get_current_user)
    ):

    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug})
    if not post:
        raise HTTPException(status_code=404,detail="Post not Found")
    
    if str(current_user.id) != str(post["author_name"]):
        raise HTTPException(status_code=403, detail="Not accessible for this user")
    
    updated_data = post_upd.dict(exclude_unset=True)

    if "title" in updated_data:
        updated_data["slug"] = slugify_title(updated_data["title"])

    posts_collection.update_one({"slug": slug}, {"$set": updated_data})

    post = posts_collection.find_one({"slug": slug})
    return convert_post(post)


@router.post("/posts/{slug}")
def DeletePost(
    slug: str,
    post_to_delete: PostUpdate,
    current_user: User = Depends(get_current_user)        
):
    
    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug})

    if not post:
        raise HTTPException(status_code= 404, detail= "Post Not found")
    
    if str(current_user.id) != str(post["author_name"]):
        raise HTTPException(status_code=403, detail="Not accessible for this user")
    
    posts_collection.delete_one({"slug": slug})
    return "Post deleted successfully"

@router.get("/me/posts")    
def get_my_posts(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10,ge=1, le=100)
):
    skip = (page-1) * limit
    query = {"author_name": str(current_user.id)}

    cursor = posts_collection.find(query).skip(skip).limit(limit)
   
    posts = []
    for post in cursor:
        posts.append(convert_post(post))
    
    return posts
   
   