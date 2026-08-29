import os
import datetime
from dotenv import load_dotenv

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', "app")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', "secret")
POSTGRES_DB = os.getenv('POSTGRES_DB', "app")
POSTGRES_HOST = os.getenv('POSTGRES_HOST', "localhost")
POSTGRES_PORT = os.getenv('POSTGRES_PORT', "5431")

POSTGRES_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)




class Base(DeclarativeBase, AsyncAttrs):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)

    @property
    def id_dict(self):
        return {"id": self.id}

class Advert(Base):
    __tablename__ = "adverts"

    title: MappedColumn[str] = mapped_column(String(50))
    description: MappedColumn[str] = mapped_column(String(255))
    created_at: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner: MappedColumn[str] = mapped_column(String(20))

    @property
    def dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "owner": self.owner

        }

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()