from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Levanthienquang@2005@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SesionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()