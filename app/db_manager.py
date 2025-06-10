from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "postgresql+asyncpg://user:12341234@rc1a-i25i7m8rrl055efp.mdb.yandexcloud.net:6432/tochka"

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,          # Максимальное число соединений
    max_overflow=10,       # Дополнительные соединения при нагрузке
    pool_timeout=30,       # Время ожидания соединения (сек)
    pool_recycle=3600,     # Пересоздавать соединения каждые 1 час
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
