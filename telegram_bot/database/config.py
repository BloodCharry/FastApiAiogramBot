import os
from dotenv import load_dotenv, find_dotenv

load_dotenv((find_dotenv()))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, '.env'))

engine = create_async_engine(os.getenv('PG_URL'), echo=True)

session_maker = async_sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=engine)
