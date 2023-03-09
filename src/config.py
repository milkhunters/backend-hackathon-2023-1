import os
from functools import lru_cache
from typing import Optional
from dataclasses import dataclass
import configparser

from src.version import __version__

import consul
from dotenv import find_dotenv, load_dotenv


@dataclass
class RedisConfig:
    HOST: Optional[str]
    PASSWORD: Optional[str]
    USERNAME: Optional[str]
    PORT: Optional[int] = 6379


@dataclass
class PostgresConfig:
    DATABASE: Optional[str]
    USERNAME: Optional[str]
    PASSWORD: Optional[str]
    HOST: Optional[str]
    PORT: Optional[int] = 5432


@dataclass
class S3Config:
    BUCKET: Optional[str]
    ENDPOINT_URL: Optional[str]
    REGION_NAME: Optional[str]
    AWS_ACCESS_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str]
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
class Email:
    isTLS: Optional[bool]
    isSSL: Optional[bool]
    HOST: Optional[str]
    PASSWORD: Optional[str]
    USER: Optional[str]
    PORT: Optional[int]


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
    EMAIL: Email
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
        if encode_value:
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
        DEBUG=bool(int(os.getenv('DEBUG', 1))),
        IS_SECURE_COOKIE=bool(config("IS_SECURE_COOKIE")),
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
                ACCESS_SECRET_KEY=config("JWT", "ACCESS_SECRET_KEY"),
                REFRESH_SECRET_KEY=config("JWT", "REFRESH_SECRET_KEY")
            )
        ),
        DB=DbConfig(
            POSTGRESQL=PostgresConfig(
                HOST=config("DATABASE", "POSTGRESQL", "HOST"),
                PORT=config("DATABASE", "POSTGRESQL", "PORT"),
                USERNAME=config("DATABASE", "POSTGRESQL", "USERNAME"),
                PASSWORD=config("DATABASE", "POSTGRESQL", "PASSWORD"),
                DATABASE=config("DATABASE", "POSTGRESQL", "DATABASE")
            ) if config("DATABASE", "POSTGRESQL", "is_used") else None,
            REDIS=RedisConfig(
                HOST=config("DATABASE", "REDIS", "HOST"),
                USERNAME=config("DATABASE", "REDIS", "USERNAME"),
                PASSWORD=config("DATABASE", "REDIS", "PASSWORD"),
                PORT=config("DATABASE", "REDIS", "PORT")
            ) if config("DATABASE", "REDIS", "is_used") else None,
            S3=S3Config(
                ENDPOINT_URL=config("DATABASE", "S3", "ENDPOINT_URL"),
                REGION_NAME=config("DATABASE", "S3", "REGION_NAME"),
                AWS_ACCESS_KEY_ID=config("DATABASE", "S3", "AWS_ACCESS_KEY_ID"),
                AWS_SECRET_ACCESS_KEY=config("DATABASE", "S3", "AWS_SECRET_ACCESS_KEY"),
                BUCKET=config("DATABASE", "S3", "BUCKET")
            ) if config("DATABASE", "S3", "is_used") else None
        ),
        EMAIL=Email(
            isTLS=bool(config("BASE", "EMAIL", "isTLS")),
            isSSL=bool(config("BASE", "EMAIL", "isSSL")),
            HOST=config("BASE", "EMAIL", "HOST"),
            PORT=config("BASE", "EMAIL", "PORT"),
            USER=config("BASE", "EMAIL", "USER"),
            PASSWORD=config("BASE", "EMAIL", "PASSWORD")
        ) if config("BASE", "EMAIL", "is_used") else None
    )


def str_to_bool(value: str) -> bool:
    return value.lower() in ("yes", "true", "t", "1")


@lru_cache()
def load_ini_config(path: str | os.PathLike, encoding="utf-8") -> Config:
    """
    Loads config from file

    :param path: *.ini
    :param encoding:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(filenames=path, encoding=encoding)

    return Config(
        DEBUG=bool(int(os.getenv('DEBUG', 1))),
        IS_SECURE_COOKIE=bool(config["BASE"]["IS_SECURE_COOKIE"]),
        BASE=Base(
            TITLE=config["BASE"]["TITLE"],
            DESCRIPTION=config["BASE"]["DESCRIPTION"],
            VERSION=__version__,
            CONTACT=Contact(
                NAME=config["CONTACT"]["NAME"],
                URL=config["CONTACT"]["URL"],
                EMAIL=config["CONTACT"]["EMAIL"]
            ),
            JWT=JWT(
                ACCESS_SECRET_KEY=config["JWT"]["ACCESS_SECRET_KEY"],
                REFRESH_SECRET_KEY=config["JWT"]["REFRESH_SECRET_KEY"]
            )
        ),
        DB=DbConfig(
            POSTGRESQL=PostgresConfig(
                HOST=config["POSTGRESQL"]["HOST"],
                PORT=int(config["POSTGRESQL"]["PORT"]),
                USERNAME=config["POSTGRESQL"]["USERNAME"],
                PASSWORD=config["POSTGRESQL"]["PASSWORD"],
                DATABASE=config["POSTGRESQL"]["DATABASE"]
            ) if str_to_bool(config["POSTGRESQL"]["is_used"]) else None,
            REDIS=RedisConfig(
                HOST=config["REDIS"]["HOST"],
                USERNAME=config["REDIS"]["USERNAME"],
                PASSWORD=config["REDIS"]["PASSWORD"],
                PORT=int(config["REDIS"]["PORT"])
            ) if str_to_bool(config["REDIS"]["is_used"]) else None,
            S3=S3Config(
                ENDPOINT_URL=config["S3"]["ENDPOINT_URL"],
                REGION_NAME=config["S3"]["REGION_NAME"],
                AWS_ACCESS_KEY_ID=config["S3"]["AWS_ACCESS_KEY_ID"],
                AWS_SECRET_ACCESS_KEY=config["S3"]["AWS_SECRET_ACCESS_KEY"],
                BUCKET=config["S3"]["BUCKET"]
            ) if str_to_bool(config["S3"]["is_used"]) else None
        ),
        EMAIL=Email(
            isTLS=str_to_bool(config["EMAIL"]["isTLS"]),
            isSSL=str_to_bool(config["EMAIL"]["isSSL"]),
            HOST=config["EMAIL"]["HOST"],
            PORT=int(config["EMAIL"]["PORT"]),
            USER=config["EMAIL"]["USER"],
            PASSWORD=config["EMAIL"]["PASSWORD"]
        ) if str_to_bool(config["EMAIL"]["is_used"]) else None
    )


@lru_cache()
def load_env_config(file_name: str = None) -> Config:
    """
    Loads config from .env file

    """
    if not file_name:
        env_file = find_dotenv()
    else:
        env_file = find_dotenv(file_name)

    if env_file:
        load_dotenv(env_file)
    else:
        raise EnvironmentError("No .env file found. Using Environment Variables.")

    return Config(
        DEBUG=bool(int(os.getenv('DEBUG', 1))),
        IS_SECURE_COOKIE=bool(os.getenv('BASE_IS_SECURE_COOKIE')),
        BASE=Base(
            TITLE=os.getenv('BASE_TITLE'),
            DESCRIPTION=os.getenv('BASE_DESCRIPTION'),
            VERSION=__version__,
            CONTACT=Contact(
                NAME=os.getenv('CONTACT_NAME'),
                URL=os.getenv('CONTACT_URL'),
                EMAIL=os.getenv('CONTACT_EMAIL')
            ),
            JWT=JWT(
                ACCESS_SECRET_KEY=os.getenv('JWT_ACCESS_SECRET_KEY'),
                REFRESH_SECRET_KEY=os.getenv('JWT_REFRESH_SECRET_KEY')
            )
        ),
        DB=DbConfig(
            POSTGRESQL=PostgresConfig(
                HOST=os.getenv('POSTGRESQL_HOST'),
                PORT=int(os.getenv('POSTGRESQL_PORT')),
                USERNAME=os.getenv('POSTGRESQL_USERNAME'),
                PASSWORD=os.getenv('POSTGRESQL_PASSWORD'),
                DATABASE=os.getenv('POSTGRESQL_DATABASE')
            ) if bool(os.getenv("is_POSTGRESQL")) else None,
            REDIS=RedisConfig(
                HOST=os.getenv('REDIS_HOST'),
                USERNAME=os.getenv('REDIS_USERNAME'),
                PASSWORD=os.getenv('REDIS_PASSWORD'),
                PORT=int(os.getenv('REDIS_PORT'))
            ) if bool(os.getenv("is_REDIS")) else None,
            S3=S3Config(
                ENDPOINT_URL=os.getenv('S3_ENDPOINT_URL'),
                REGION_NAME=os.getenv('S3_REGION_NAME'),
                AWS_ACCESS_KEY_ID=os.getenv('S3_AWS_ACCESS_KEY_ID'),
                AWS_SECRET_ACCESS_KEY=os.getenv('S3_AWS_SECRET_ACCESS_KEY'),
                BUCKET=os.getenv('S3_BUCKET')
            ) if bool(os.getenv('is_S3')) else None
        ),
        EMAIL=Email(
            isTLS=bool(os.getenv('EMAIL_isTLS')),
            isSSL=bool(os.getenv('EMAIL_isSSL')),
            HOST=os.getenv('EMAIL_HOST'),
            PORT=int(os.getenv('EMAIL_PORT')),
            USER=os.getenv('EMAIL_USER'),
            PASSWORD=os.getenv('EMAIL_PASSWORD')
        ) if bool(os.getenv('is_EMAIL')) else None
    )
