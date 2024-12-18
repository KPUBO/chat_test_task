from pydantic import BaseModel
from pydantic import PostgresDsn

from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False,
    echo_pool: bool = False,
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
