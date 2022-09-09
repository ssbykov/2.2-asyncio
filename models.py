from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


engine = create_async_engine(f"postgresql+asyncpg://"
                             f"{os.getenv('DB_USER')}"
                             f":{os.getenv('DB_PASS')}"
                             f"@{os.getenv('DB_HOST')}"
                             f":{os.getenv('DB_PORT')}"
                             f"/{os.getenv('DB_BASE')}")

Base = declarative_base()

class People(Base):
    __tablename__ = 'peoples'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    birth_year = Column(String(15))
    eye_color = Column(String(15))
    films = Column(String())
    gender = Column(String(20))
    hair_color = Column(String(15))
    height = Column(String(10))
    homeworld = Column(String(100))
    mass = Column(String(10))
    skin_color = Column(String(25))
    species = Column(String())
    starships = Column(String())
    vehicles = Column(String())

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
