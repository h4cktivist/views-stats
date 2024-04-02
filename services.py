from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import argon2
from jose import jwt
from decouple import config
from models import models, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password):
    return argon2.hash_password(password.encode())


def verify_password(plain_password, hashed_password):
    return argon2.verify_password(hashed_password, plain_password.encode())


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, config('SECRET_KEY'), algorithm=config('ALGORITHM'))
    return {
        'type': 'Bearer',
        'token': encoded_jwt
    }


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, config('SECRET_KEY'), algorithms=[config('ALGORITHM')])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.JWTError:
        return {'error': 'Invalid token'}


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    if payload.get('error'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return payload


def login(db: Session, login_data: schemas.UserCreate):
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if user:
        if verify_password(login_data.password, user.hashed_password):
            token = create_jwt_token({'sub': user.username}, expires_delta=timedelta(hours=1))
            return token
        else:
            raise HTTPException(status_code=401, detail='Invalid password')
    else:
        raise HTTPException(status_code=404, detail='User is not found')
