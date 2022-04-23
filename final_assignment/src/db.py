from typing import Any, Generator
from uuid import uuid4

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

import constants as const


def get_uuid():
    return str(uuid4())


@as_declarative()
class Base:

    __name__: str
    id = db.Column(db.String(36), primary_key=True, index=True, default=get_uuid)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engine = create_engine(const.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:

    db = SessionLocal()

    yield db

    db.close()
