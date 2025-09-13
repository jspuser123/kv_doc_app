from sqlalchemy import Column,String,Integer,Float,Numeric,Boolean, DateTime,ForeignKey, table, true,create_engine
#from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.sql import func, text
from contextlib import contextmanager,asynccontextmanager
from sqlalchemy.orm import Session
#import os
#from dotenv import load_dotenv

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
class document_name(Base):
    __tablename__ = 'document_name'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    name=Column(String(255))
    description=Column(String(255))
class document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    name=Column(String(255))
    description=Column(String(255))
    io=Column(String(255))
    style=Column(String(255))
    color=Column(String(255))
    pi=Column(String(255))
    po_qty=Column(Float)
    delivery_qty=Column(Float)
    usd=Column(Float)
    po_value_usd=Column(Float)
    delivery_usd=Column(Float)
    excess_stock=Column(Float)
    stock_value_usd=Column(Float)
    inr=Column(Float)
    percent=Column(Float)
    value=Column(String(255))
    date=Column(DateTime)
    document_child=relationship('document_child',back_populates='document',cascade="all, delete-orphan")

class document_child(Base):
    __tablename__ = 'document_child'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    name=Column(String(255))
    file=Column(String(255))
    document_id=Column(Integer,ForeignKey('document.id'))
    document=relationship('document',back_populates='document_child')
class path_server(Base):
    __tablename__ = 'path_server'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    path=Column(String(255))
    description=Column(String(255))


DATABASE_URL ="sqlite:///../data.db"
#"sqlite:///../data.db"
#DATABASE_URL = f"mysql+mysqlconnector://{username}:{passwd}@{host}:{port}/{database}"
#f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
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

# x=load_dotenv()

#     server = os.getenv("SERVER")
#     database = os.getenv("database")
#     username = os.getenv("user")
#     password = os.getenv("password")
#     driver = os.getenv("driver")
#     driver1 = os.getenv("driver1")
#     driver2 = os.getenv("driver2")
#     DATABASE_URL = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver2}'
