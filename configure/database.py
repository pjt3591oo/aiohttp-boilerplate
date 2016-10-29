from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configure.conf as conf

url = conf.database[0]["category"]+"://"+conf.database[0]["user"]+":"+conf.database[0]["password"]+"@"+conf.database[0]["host"]+"/"+conf.database[0]["database"]

engine = create_engine(url, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  from models import models

  Base.metadata.create_all(engine)
