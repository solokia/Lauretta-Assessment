""" This file defines data base connection details and exposes an engine and session object """

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()
package = 'postgresql'
port = 5432

host = os.environ['HOST']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
database = os.environ['DB']

SQLALCHEMY_DATABASE_URL = f'{package}://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
