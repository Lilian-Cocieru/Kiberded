
# C:\Users\Computer\Desktop\python\Kiberded\database\engine.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from database.models import Base 

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DB_URL, echo=False) 

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        # Эта строка создает все таблицы, определенные в Base.metadata, если их нет.
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована (таблицы проверены/созданы).")









# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import declarative_base
# from config import DB_URL

# Base = declarative_base()

# engine = create_async_engine(DB_URL, echo=True)
# session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# async def create_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
