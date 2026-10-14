from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Request
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    url: str


class AuthSettings(BaseSettings):
    jwt_token: str


class AppSettings(BaseSettings):
    name: str = "My Posts API"
    description: str = "API аналог приложения Twitter"
    debug: bool = False


class DebounceTimeSettings(BaseSettings):
    minimal_post_debounce_time: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    database_url: str
    database_url_sync: str
    jwt_secret: str
    minimal_post_debounce_time: int

    @property
    def app(self) -> AppSettings:
        return AppSettings()

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(jwt_token=self.jwt_secret)

    @property
    def debounce(self) -> DebounceTimeSettings:
        return DebounceTimeSettings(
            minimal_post_debounce_time=self.minimal_post_debounce_time
        )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme not in {"postgresql", "postgresql+asyncpg"}:
            raise ValueError(
                "database_url scheme must be postgresql | postgresql+asyncpg"
            )

        if not parsed.hostname:
            raise ValueError("database_url must include hostname")

        db_name = (parsed.path or "").lstrip("/")

        if not db_name:
            raise ValueError("database_url must include database")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("database_url must be 1..65535")

        return v

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt(cls, v: str) -> str:

        if not v.strip():
            raise ValueError("JWT_SECRET must be")

        return v

    @field_validator("minimal_post_debounce_time")
    @classmethod
    def validate_minimal_post_debounce_time(cls, v: str) -> int:

        if v < 0:
            raise ValueError("minimal_post_debounce_time (minutes) must be > 0")

        return v


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


SettingsDeps = Annotated[Settings, Depends(get_settings)]
