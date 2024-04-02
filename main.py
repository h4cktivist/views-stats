from fastapi import Depends, FastAPI, BackgroundTasks
from sqlalchemy.orm import Session

from models import models, schemas
from database import SessionLocal, engine
import services
import parsers


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db=db, user=user)


@app.post('/users/login')
async def login(login_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.login(db=db, login_data=login_data)


@app.post('/get-views/vk')
async def get_views_vk(data: schemas.LinksList, background_tasks: BackgroundTasks,
                       current_user=Depends(services.get_current_user)):
    for post_url in data.links:
        background_tasks.add_task(parsers.parse_views_vk, post_url=post_url)
    return {'message': 'Links were sent to the background'}
