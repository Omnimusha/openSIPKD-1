from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
class osPbbUser(Base):
    __tablename__ = 'user_pbb'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    created = Column(DateTime)
    disabled = Column(Integer)
    kd_kanwil = Column(String(2))
    kd_kantor = Column(String(2))
    kd_kppbb = Column(String(2))
    kd_bank_tunggal = Column(String(2))
    kd_bank_persepsi = Column(String(2))
    kd_tp = Column(String(2))
 
    def __init__(self,data):
        self.id=data['id']
        self.user_id=data['user_id']
        self.created=data['created']
        self.disabled=data['disabled']
        self.kd_kppbb=data['kd_kppbb']
        self.kd_kanwil=data['kd_kanwil']
        self.kd_tp=data['kd_tp']
        self.kd_bank_tunggal=data['kd_bank_tunggal']
        self.kd_bank_persepsi=data['kd_bank_persepsi']
        self.kd_kantor=data['kd_kantor']

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
    def hapus(cls,datas,kode):
        DBSession.query(cls).filter( and_(          
              cls.kd_propinsi==kode['kd_propinsi'],
              cls.kd_dati2==kode['kd_dati2'],
              cls.kd_kecamatan==kode['kd_kecamatan'],
            )).delete()

    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).all()
        
    @classmethod
    def get_by_user_id(cls,id):
        return DBSession.query(cls).filter(
              cls.user_id==id,
              ).first()

    