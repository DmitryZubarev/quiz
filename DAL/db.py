from sqlalchemy.orm import sessionmaker
from classes import *
import datetime
import pg8000

session = sessionmaker(bind=engine)
s = session()

print(s.query(Session).first().session_user[0].name)
