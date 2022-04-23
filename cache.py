import redis

import constants as const


redis_client = redis.Redis(
    host=const.REDIS_HOST,
    port=const.REDIS_PORT,
    db=const.REDIS_DB,
    username=const.REDIS_USER,
    password=const.REDIS_PASSWORD,
    charset="utf-8",
    decode_responses=True,
)
