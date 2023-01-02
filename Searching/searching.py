from DAL import *

from sqlalchemy.orm import sessionmaker

DATA = connect()
session = sessionmaker(bind=engine)
s = session()

print(s.query(Session)[0].session_user[0].name)
