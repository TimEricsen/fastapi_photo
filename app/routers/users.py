from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt

from .dependencies import get_db, authenticate_user, create_access_token, get_hashed_password, get_user
from ..schemas import UserCreate, UserMain, TokenData
from ..models import User


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, 'SECRET', 'HS256')
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        token_data = TokenData(username=username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
            )
    user = get_user(token_data.username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return user


@router.post('/registration', tags=['Registration/Authentication'])
async def user_registration(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(user.password)
    user_by_username = db.query(User).filter(User.username == user.username).first()
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This username is already used'
        )
    user_by_email = db.query(User).filter(User.email == user.email).first()
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This email is already used'
        )
    try:
        db_user = User(username=user.username, email=user.email,
                       full_name=user.full_name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Oops, there is something wrong...'
        )


@router.post('/token', tags=['Registration/Authentication'])
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password'
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={'sub': user.username},
                                       expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me', tags=['My account'], response_model=UserMain)
async def get_my_profile(current_user: UserMain = Depends(get_current_user)):
    return current_user



