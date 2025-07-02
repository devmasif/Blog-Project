import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from db.mongo import users_collection
from fastapi.security import OAuth2PasswordBearer
from models.user_models import User

load_dotenv()

secret_key = os.getenv("JWT_SECRET_KEY")
algorithm = os.getenv("JWT_ALGORITHM")
expire_minutes_str = os.getenv("JWT_EXPIRE_MINUTES")

if secret_key is None or algorithm is None or expire_minutes_str is None:
    raise RuntimeError("Missing one or more JWT configuration environment variables.")

SECRET_KEY: str = secret_key
ALGORITHM: str = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: float = float(expire_minutes_str)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_pw: str, hash_pw: str) -> bool:
    return bcrypt_context.verify(plain_pw, hash_pw)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": data["email"]})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        user = users_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User.model_validate({
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "bio": user.get("bio", ""),
            "created_at": user["created_at"]
        })
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
