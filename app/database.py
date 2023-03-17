from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_CONNECTION_URL = 'postgresql://postgres:password@db:5432/fastapi-postgres'

engine = create_engine(url=DB_CONNECTION_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()
