from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_model = True


class UserCreate(BaseModel):
    username: str
    password: str


class LinksList(BaseModel):
    links: list[str]
