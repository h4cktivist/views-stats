from sqlalchemy.orm import Session
from models import models, schemas
import argon2


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
