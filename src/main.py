from fastapi import FastAPI, Request, Response
from fastapi_redis_cache import FastApiRedisCache
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import constants as const
import views
import models # noqa
import db


app = FastAPI(title=const.APPLICATION_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(views.api_router)
db.Base.metadata.create_all(bind=db.engine)


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=const.REDIS_URI,
        prefix=const.APPLICATION_NAME,
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response, Session]
    )
