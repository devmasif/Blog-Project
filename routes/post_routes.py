from fastapi import APIRouter, HTTPException, Depends, Query, status
from models.post_models import PostCreate, PostOut, PostUpdate
from util.slugify import slugify_title, convert
from db.mongo import posts_collection
from typing import List, Optional, Any
from models.user_models import User
from util.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get(
    "/posts",
    response_model=List[PostOut],
    summary="List published posts",
    description="""
Retrieve a list of **published posts**.

- Filter by author or tag
- Supports pagination (page & limit)
""",
    tags=["Posts"]
)
def list_published_posts(
    author: Optional[str] = Query(None, description="Filter by author ID"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of posts per page")
):
    query: dict[str, Any] = {"is_published": True}
    if author:
        query["author_name"] = author
    if tag:
        query["tags"] = tag

    skip = (page - 1) * limit
    cursor = posts_collection.find(query).skip(skip).limit(limit)
    return [convert(post) for post in cursor]


@router.get(
    "/posts/{slug}",
    response_model=PostOut,
    summary="Get a published post by slug",
    description="Returns a specific published post using the provided slug.",
    tags=["Posts"]
)
def get_post(slug: str):
    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug, "is_published": True})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return convert(post)


@router.post(
    "/posts",
    response_model=PostOut,
    summary="Create a new post",
    description="Creates and publishes a new post. Requires authentication.",
    tags=["Posts"]
)
def create_post(
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
    return convert(post_data)


@router.put(
    "/posts/{slug}",
    response_model=PostOut,
    summary="Edit an existing post",
    description="Updates a post (title, content, tags) by slug. Only the author can edit.",
    tags=["Posts"]
)
def edit_post(
    slug: str,
    post_upd: PostUpdate,
    current_user: User = Depends(get_current_user)
):
    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if str(current_user.id) != str(post["author_name"]):
        raise HTTPException(status_code=403, detail="Not accessible for this user")

    updated_data = post_upd.dict(exclude_unset=True)

    if "title" in updated_data:
        updated_data["slug"] = slugify_title(updated_data["title"])

    updated_data["updated_at"] = datetime.utcnow()
    posts_collection.update_one({"slug": slug}, {"$set": updated_data})

    post = posts_collection.find_one({"slug": updated_data.get("slug", slug)})
    return convert(post)


@router.delete(
    "/posts/{slug}",
    summary="Delete a post",
    description="Deletes a post by slug. Only the author is allowed to delete.",
    tags=["Posts"]
)
def delete_post(
    slug: str,
    current_user: User = Depends(get_current_user)
):
    slug = slugify_title(slug)
    post = posts_collection.find_one({"slug": slug})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if str(current_user.id) != str(post["author_name"]):
        raise HTTPException(status_code=403, detail="Not accessible for this user")

    posts_collection.delete_one({"slug": slug})
    return {"message": "Post deleted successfully"}


@router.get(
    "/me/posts",
    response_model=List[PostOut],
    summary="Get my posts",
    description="Lists posts authored by the currently authenticated user.",
    tags=["Posts"]
)
def get_my_posts(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    skip = (page - 1) * limit
    query = {"author_name": str(current_user.id)}
    cursor = posts_collection.find(query).skip(skip).limit(limit)
    return [convert(post) for post in cursor]
