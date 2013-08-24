import json
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    String,
    Index,
    ForeignKey,
    func,
    Table,
    Float,
    BigInteger,
    Numeric,
    Date
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

gkd_propinsi = '32'
gkd_dati2 = '79'


def to_json(inst, cls):
    
    """
    Jsonify the sql alchemy query result.
    """
    #convert = dict()
    #print x
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    #d = dict()
    """for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    #print d"""
    return {'a':'a'}  #json.dumps(d)
    
class osSipkdModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    create_uid = Column(Integer)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime)
    update_uid = Column(Integer)
    kode = Column(String(32), unique=True)
    nama = Column(String(64))

    def __init__(self, nama, kode):
        self.nama = nama
        self.kode = kode
