from typing import Annotated, AsyncGenerator

from fastapi import Depends

from app.core.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select

settings = Settings()  # type: ignore[call-arg]
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)

async_session_local = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as session:
        yield session


async def check_db(session: AsyncSession) -> int:
    res = await session.execute(select(1))
    return res.scalar_one()

DbSessionDeps = Annotated[
    AsyncSession, Depends(get_session)
]

class Base(DeclarativeBase):
    pass