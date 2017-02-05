
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

_Base = automap_base()
_engine = create_engine('mysql://helo_db:helo_db@localhost/esp')
_Base.prepare(_engine, reflect=True)
_session = Session(_engine)

class DataAccessLayer(object):
    session = _session
    tbls = _Base.classes