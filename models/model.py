from sqlalchemy import Column,String,Integer,Float,Boolean, DateTime,ForeignKey, table, true,create_engine
#from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.sql import func, text
from contextlib import contextmanager,asynccontextmanager
from sqlalchemy.orm import Session


Base = declarative_base() 

class auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    user = Column(String(255))
    email = Column(String(255),unique=True)
    password = Column(String(255),unique=True)
    ph = Column(String(255))
    init_date = Column(DateTime)
    expire_date = Column(DateTime, onupdate=func.now())
    company = Column(String(255))
    token=Column(String(255))
    version=Column(Integer)


DATABASE_URL = "sqlite:///data.db"
#DATABASE_URL = f"mysql+mysqlconnector://{username}:{passwd}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_db():
    #Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
  
@contextmanager
def get_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
create_all_db()
#engine = create_async_engine(DATABASE_URL,future=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

#asyncio.run(async_create_all())
# @asynccontextmanager
# async def get_session():
#     async with SessionLocal() as session:
#         yield session

