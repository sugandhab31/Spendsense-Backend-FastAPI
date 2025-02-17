from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database="spendsense",
user="flask-user",
password="postgres",
host="127.0.0.1",
port=5432,

URL_DATABASE = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    user[0],password[0],host[0],port[0],database[0]
)
print(URL_DATABASE)
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()