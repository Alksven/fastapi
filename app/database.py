from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from app.config import settings

DB_HOST ="localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = 2295
DB_NAME = "postgres"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# import asyncio
#
# async def test_connection():
#     async with engine.begin() as conn:
#         await conn.run_sync(lambda conn: print("✅ Успешное подключение к БД!"))
#
# asyncio.run(test_connection())