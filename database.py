import os
from dotenv import load_dotenv
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

load_dotenv()
DB_URL = os.getenv('DEVELOP_DB_URL')

engine = create_engine(DB_URL, pool_recycle=500)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 연결              
class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn 
    
# DB 세션 관리
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
