from pydantic import PostgresDsn, RedisDsn


APPLICATION_NAME = 'efarms_assignment'

REDIS_USER = 'default'
REDIS_PASSWORD = 'password123'
REDIS_PORT = '6379'
REDIS_HOST = 'redis'
REDIS_DB = 0

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme='postgresql+psycopg2',
    user='admin',
    password='admin',
    host='db',
    port='5432',
    path=f'/{APPLICATION_NAME}'
)

REDIS_URI = RedisDsn.build(
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    host=REDIS_HOST,
    port=REDIS_PORT,
    path=f'/{REDIS_DB}',
    scheme='redis'
)
