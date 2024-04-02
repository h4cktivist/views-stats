from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import models, schemas
from database import SessionLocal, engine
import services


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db=db, user=user)
