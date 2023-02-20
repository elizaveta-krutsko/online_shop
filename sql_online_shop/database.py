from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config as conf


SQLALCHEMY_DATABASE_URL = f'{conf.DB_DIALECT}://{conf.DB_USERNAME}:{conf.DB_PASSWORD}@{conf.DB_HOST}:{conf.DB_PORT}/{conf.DB_NAME}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
