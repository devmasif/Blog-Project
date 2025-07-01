from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException
from db.mongo import users_collection
from fastapi.security import OAuth2PasswordBearer
from models.user_models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
                                     
bcrypt_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "abcdef@123@2@#$!#1233124214"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_pw : str, hash_pw: str) -> bool:
    return bcrypt_context.verify(plain_pw,hash_pw)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) ->User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code= 401, detail= "Token invalid")
        
        user = users_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code= 401, detail= "User Not Found")
        
        return User(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            bio=user.get("bio", ""),
            created_at=user["created_at"]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


