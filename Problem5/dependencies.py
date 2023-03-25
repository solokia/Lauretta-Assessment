""" Starts a session for the DB call """
from database import SessionLocal

def get_session():
    """ Creates a db session """
    try:
        _db = SessionLocal()
        yield _db
    finally:
        _db.close()
