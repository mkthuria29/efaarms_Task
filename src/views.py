from typing import List

from fastapi import APIRouter, Depends
from fastapi_redis_cache import cache
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from cache import redis_client
import constants as const
import models
import schemas

api_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@api_router.get('/list/users', response_model=List[schemas.UserInDBBase])
def list_user(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    res = db.query(models.User).offset(skip).limit(limit).all()
    return res


@api_router.post('/create/user')
def create_user(
        obj_in: schemas.UserCreate,
        db: Session = Depends(get_db),
):
    db_obj = models.User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
    )
    db.add(db_obj)
    db.commit()

    return 'successfully created'


@api_router.get('/list/books', response_model=List[schemas.BookInDBBase])
@cache()
def list_book(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    res = db.query(models.Book).offset(skip).limit(limit).all()

    return res


@api_router.post('/create/book')
def create_book(
        obj_in: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_obj = models.Book(
        **obj_in.dict()
    )

    for key in redis_client.scan_iter(
        f"{const.APPLICATION_NAME}:{list_book.__module__}.{list_book.__name__}*"
    ):
        redis_client.delete(key)

    db.add(db_obj)
    db.commit()

    return 'successfully created'


@api_router.post('/add-to-favourites')
def create_book(
        obj_in: schemas.AddToFavourite,
        db: Session = Depends(get_db),
):
    db_obj = db.query(models.FavouriteBook).first()

    if not db_obj:
        db_obj = models.FavouriteBook(
            user_id=obj_in.user_id,
            book_id=obj_in.book_id,
        )
        db.add(db_obj)

    db_obj.like = obj_in.like
    db.commit()

    return 'successfully updated'


@api_router.get('/user/list-favourites', response_model=List[schemas.BookInDBBase])
def list_favourites(
        user_id: str,
        db: Session = Depends(get_db),
):
    db_obj = db.query(models.FavouriteBook) \
        .filter(models.FavouriteBook.user_id == user_id,
                models.FavouriteBook.like == True) \
        .all()

    return [i.book for i in db_obj]


@api_router.get('/user-favourite-count', response_model=List[schemas.UserFavouriteCount])
def user_favourite_count(
        db: Session = Depends(get_db),
):
    db_obj = db.query(models.FavouriteBook.user_id,
                      func.count(models.FavouriteBook.id).label('count')) \
        .filter(models.FavouriteBook.like == True) \
        .group_by(models.FavouriteBook.user_id) \
        .all()

    return db_obj
