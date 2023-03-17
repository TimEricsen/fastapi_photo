from ..database import SessionLocal
from ..models import User
from ..schemas import UserMain

from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from datetime import datetime
from jose import jwt


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_user(username, db):
    user = db.query(User).filter(User.username == username).first()
    if user:
        db_user = jsonable_encoder(user)
        return UserMain(**db_user)


def authenticate_user(username, password, db):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, 'SECRET', algorithm='HS256')
    return encoded_jwt




