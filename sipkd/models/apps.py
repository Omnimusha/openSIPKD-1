import sys
from model import * 


class osApps(Base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime)
    create_uid = Column(Integer)
    update_uid = Column(Integer)
    kode = Column(String(64))
    nama = Column(String(64))
    locked = Column(Integer, default=0)
    
    def __init__(self, nama, kode, locked):
        self.nama = nama
        self.kode = kode
        self.locked = locked
    
    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).order_by('kode').all()
        
    @classmethod
    def get_by_id(cls,id):
        return DBSession.query(cls).filter(cls.id==id).first()
        
    @classmethod
    def get_by_nama(cls,nama):
        return DBSession.query(cls).filter(cls.nama==nama).first()
    
    @classmethod
    def get_by_kode(cls,kode):
            return DBSession.query(cls).filter(cls.kode==kode).first()        

    @classmethod
    def edit(cls, data):
        DBSession.merge(cls(data))
        
    @classmethod
    def edit_locked(cls, data):
        a = DBSession.query(cls).filter_by(id=data['id']).first()
        a.locked = data['value']
        try: 
            DBSession.merge(a)
            return True
        except:
            print sys.exc_info()
            return False
        
class osModules(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime)
    create_uid = Column(Integer)
    update_uid = Column(Integer)
    kode = Column(String(20))
    nama = Column(String(50))
    locked = Column(Integer, default=0)
    app_id = Column(Integer,
                ForeignKey('apps.id', onupdate="CASCADE", ondelete="CASCADE"),
              )
    
    Index('modules_app_id_kode_ukey', kode , app_id, unique=True )

    def __init__(self, nama, kode, locked, parent):
        self.nama = nama
        self.kode = kode
        self.locked = locked
        ids = osApps.get_by_kode(parent)
        self.app_id = ids.id
        
