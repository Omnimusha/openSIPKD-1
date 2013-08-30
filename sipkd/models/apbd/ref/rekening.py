from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
class osRefRekening(Base):
    __tablename__ = 'rekenings'
    #__autoload__  = True
    id = Column(Integer, primary_key=True)
    kode = Column(String(15))
    nama = Column(String(150))
    level_id = Column(Integer)
    defsign = Column(Integer)
    header_id = Column(Integer)
    locked = Column(Integer)

    def __init__(self,data):
        self.id = data['id']
        self.kode = data['kode']
        self.nama = data['nama']
        self.level_id = data['level_id']
        self.defsign = data['defsign']
        self.header_id = data['header_id']
        self.locked = data['locked']

      
    @classmethod
    def row2dict(cls,row):
        d = {}
        if row:
            for column in row.__table__.columns:
                d[column.name] = getattr(row, column.name)
        return d
        
    @classmethod
    def tambah(cls, datas):
        data=cls(cls(datas))
        DBSession.add()
            
    @classmethod
    def edit(cls, data):
        DBSession.merge(cls(data))
            
    @classmethod
    def hapus(cls, data):
        DBSession.query(cls).filter(           
              cls.id==data['id']
            ).delete()

    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).order_by('kode').all()
        
    @classmethod
    def get_by_kode(cls, data):
        return DBSession.query(cls).filter(
                  cls.kode==data['kode']
                ).first()
        
    @classmethod
    def get_by_id(cls, data):
        return DBSession.query(cls).filter(
                  cls.id==data['id']
                ).first()

    @classmethod
    def get_by_nama(cls, data):
        return DBSession.query(cls).filter(
                       cls.nama.like( '%s%' % data['nama'])
                       ).first()
    