from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import User, UserRegister
from db.mongo import users_collection
from util.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from datetime import datetime

router = APIRouter(tags=["Auth"])


@router.post(
    "/Register",
    summary="Register a new user",
    description="""
### 🔐 Register a New User

Creates a user account by:

- Verifying that the **email** and **username** are unique.
- Hashing the password securely.
- Saving the user data in MongoDB.

#### 📥 Request Body
```json
{
  "email": "user@example.com",
  "username": "uniqueuser",
  "password": "StrongPass123!"
}
📤 Responses
✅ 200 OK:

json
Copy
Edit
{ "message": "User registered successfully" }
❌ 400 Bad Request:

json
Copy
Edit
{ "detail": "User Already Registered" }
"""
)
def register_user(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User Already Registered")


    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username Already Exists")

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

@router.post(
"/Login",
summary="Authenticate and log in a user",
description="""

🔑 Login
Authenticates a user with email and password.

Accepts form-encoded input (application/x-www-form-urlencoded)

Validates user credentials

Returns a JWT access token

📥 Form Fields
username = Email

password = User password

📤 Responses
✅ 200 OK:

json
Copy
Edit
{
  "message": "Login successful",
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
❌ 401 Unauthorized:

json
Copy
Edit
{ "detail": "Invalid credentials" }
"""
)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
"/me",
response_model=User,
summary="Get current user's profile",
description="""

👤 Get Current User
Returns the authenticated user's profile.

Requires Authorization: Bearer <token> header

📤 Response (User)
json
Copy
Edit
{
  "email": "user@example.com",
  "username": "uniqueuser",
  "bio": "",
  "created_at": "2025-07-04T08:00:00Z"
}
✅ 200 OK: Returns user profile

❌ 401 Unauthorized: Invalid or missing token
"""
)
def view_profile(current_user: User = Depends(get_current_user)):
    return current_user