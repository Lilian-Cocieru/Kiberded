
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import DB_URL

class Base(DeclarativeBase, AsyncAttrs):
    pass

engine = create_async_engine(DB_URL, echo=False)  # echo=True для отладки
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)







# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import declarative_base
# from config import DB_URL

# Base = declarative_base()

# engine = create_async_engine(DB_URL, echo=True)
# session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# async def create_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
