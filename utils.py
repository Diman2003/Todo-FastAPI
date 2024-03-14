from passlib.context import CryptContext
from schemas import *
from engine import session as SessionLocal
from models import *
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jws, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Replace with a strong, unique secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 36000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Functions for password hashing and verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Function to authenticate user
def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def add_token_to_blacklist(token: str, expire_minutes: int = 15):
    # Replace with your database logic to add token to blacklist
    # Set expiration time (e.g., 15 minutes)
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    blacklisted_token = BlacklistToken(token=token, expires_at=expires_at)    # ... (store blacklisted_token in database)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Fetch user from database (replace with your implementation)
        db=SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception