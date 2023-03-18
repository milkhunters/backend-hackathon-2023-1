import os
from functools import lru_cache
from typing import Optional
from dataclasses import dataclass

from src.version import __version__

import consul


@dataclass
class RedisConfig:
    HOST: Optional[str]
    PASSWORD: Optional[str]
    USERNAME: Optional[str]
    PORT: int = 6379


@dataclass
class PostgresConfig:
    DATABASE: Optional[str]
    USERNAME: Optional[str]
    PASSWORD: Optional[str]
    HOST: Optional[str]
    PORT: int = 5432


@dataclass
class S3Config:
    BUCKET: Optional[str]
    HOST: Optional[str]
    PORT: Optional[int]
    REGION: Optional[str]
    ACCESS_KEY: Optional[str]
    SECRET_ACCESS_KEY: Optional[str]
    SERVICE_NAME: Optional[str] = "s3"


@dataclass
class DbConfig:
    POSTGRESQL: Optional[PostgresConfig]
    REDIS: Optional[RedisConfig]
    S3: Optional[S3Config]


@dataclass
class Contact:
    NAME: Optional[str]
    URL: Optional[str]
    EMAIL: Optional[str]


@dataclass
class JWT:
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str


@dataclass
class Base:
    TITLE: Optional[str]
    DESCRIPTION: Optional[str]
    VERSION: Optional[str]
    JWT: JWT
    CONTACT: Contact


@dataclass
class Config:
    DEBUG: bool
    IS_SECURE_COOKIE: bool
    BASE: Base
    DB: DbConfig


class KVManager:
    def __init__(self, kv, *, root_name: str):
        self.config = kv
        self.root_name = root_name

    def __call__(self, *args: str) -> int | str | None:
        """
        :param args: list of nodes
        """
        path = "/".join([self.root_name, *args])
        encode_value = self.config.get(path)[1]
        if encode_value and encode_value["Value"]:
            value: str = encode_value['Value'].decode("utf-8")
            if value.isdigit():
                return int(value)
            return value
        return None


@lru_cache()
def load_consul_config(
        root_name: str,
        *,
        host='127.0.0.1',
        port=8500,
        token=None,
        scheme='http',
        **kwargs
) -> Config:
    """
    Load config from consul

    :param root_name: root name of dir in consul
    :param host: consul host
    :param port: consul port
    :param token: consul token
    :param scheme: consul scheme
    :param kwargs: other consul kwargs
    """

    config = KVManager(
        consul.Consul(
            host=host,
            port=port,
            token=token,
            scheme=scheme,
            **kwargs
        ).kv,
        root_name=root_name
    )
    return Config(
        DEBUG=bool(int(os.getenv("DEBUG", 1))),
        IS_SECURE_COOKIE=bool(int(os.getenv("IS_SECURE_COOKIE", 1))),
        BASE=Base(
            TITLE=config("BASE", "TITLE"),
            DESCRIPTION=config("BASE", "DESCRIPTION"),
            VERSION=__version__,
            CONTACT=Contact(
                NAME=config("BASE", "CONTACT", "NAME"),
                URL=config("BASE", "CONTACT", "URL"),
                EMAIL=config("BASE", "CONTACT", "EMAIL")
            ),
            JWT=JWT(
                ACCESS_SECRET_KEY=config("BASE", "JWT", "ACCESS_SECRET_KEY"),
                REFRESH_SECRET_KEY=config("BASE", "JWT", "REFRESH_SECRET_KEY")
            )
        ),
        DB=DbConfig(
            POSTGRESQL=PostgresConfig(
                HOST=config("DB", "POSTGRESQL", "HOST"),
                PORT=config("DB", "POSTGRESQL", "PORT"),
                USERNAME=config("DB", "POSTGRESQL", "USERNAME"),
                PASSWORD=config("DB", "POSTGRESQL", "PASSWORD"),
                DATABASE=config("DB", "POSTGRESQL", "DATABASE")
            ),
            REDIS=RedisConfig(
                HOST=config("DB", "REDIS", "HOST"),
                USERNAME=config("DB", "REDIS", "USERNAME"),
                PASSWORD=config("DB", "REDIS", "PASSWORD"),
                PORT=config("DB", "REDIS", "PORT")
            ),
            S3=S3Config(
                HOST=config("S3", "HOST"),
                PORT=config("S3", "PORT"),
                REGION=config("S3", "REGION"),
                ACCESS_KEY=config("S3", "ACCESS_KEY"),
                SECRET_ACCESS_KEY=config("S3", "SECRET_ACCESS_KEY"),
                BUCKET=config("S3", "BUCKET")
            )
        )
    )
