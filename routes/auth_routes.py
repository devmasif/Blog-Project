from fastapi import APIRouter,HTTPException,Depends
from models.user_models import User,UserLogin,UserRegister
from db.mongo import users_collection
from util.auth import hash_password,verify_password,create_access_token,get_current_user
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post(
    "/Register"
)
def register_user(user: UserRegister):
    """
    Register a new user.

    - Checks if the provided email or username already exists.
    - Hashes the password and stores the new user in the database.

    Args:
        user (UserRegister): Registration data (email, username, password).

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If email or username already exists.
    """
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User Already Registered")

    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="UserName Already Exists")

    hashed_password = hash_password(user.password)

    user_doc = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "bio": "",
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user_doc)
    return {"message": "User registered successfully"}


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/Login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})  # username carries email
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
def view_profile(current_user: User = Depends(get_current_user)):
    return current_user

