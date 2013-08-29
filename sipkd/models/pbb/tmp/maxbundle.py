from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
class osMaxBundle(Base):
    __tablename__ = 'temp_max_bundel'
    kd_kanwil = Column(String(2), primary_key=True)
    kd_kantor = Column(String(2), primary_key=True)
    temp_thn_bundel = Column(String(4), primary_key=True)
    temp_no_bundel = Column(String(4), primary_key=True)
    temp_urut_bundel = Column(String(3), primary_key=True)

    def __init__(self,data):
        self.kd_kanwil=data['kd_kanwil'],
        self.kd_kantor=data['kd_kantor'],
        self.temp_thn_bundel=data['temp_thn_bundel'],
        self.temp_no_bundel=data['temp_no_bundel'],
        self.temp_urut_bundel=data['temp_urut_bundel'],

      
    @classmethod
    def row2dict(cls,row):
        d = {}
        if row:
            for column in row.__table__.columns:
                d[column.name] = getattr(row, column.name)
        return d
        
    @classmethod
    def kode_split(cls,kode):
        return {'kd_propinsi':kode[0:2],
                'kd_dati2':kode[2:4],
                'kd_kecamatan':kode[4:7],
                'kd_kelurahan':kode[7:10],}
                
    @classmethod
    def kode_join(cls,kode):
        return ''.join((kode['kd_propinsi'],
                        kode['kd_dati2'],
                        kode['kd_kecamatan'],
                        kode['kd_kelurahan'],
                      ))

    @classmethod
    def tambah(cls, datas):
        data=cls(cls(datas))
        DBSession.add()
            
    @classmethod
    def edit(cls, data):
        DBSession.merge(cls(data))
            
    @classmethod
    def hapus(cls,datas,data):
        DBSession.query(cls).filter( and_(          
            cls.kd_kanwil==data['kd_kanwil'],
            cls.kd_kantor==data['kd_kantor'],
            cls.temp_thn_bundel==data['temp_thn_bundel'],
            cls.temp_no_bundel==data['temp_no_bundel'],
            cls.temp_urut_bundel==data['temp_urut_bundel'],
            )).delete()

    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).all()
        
    @classmethod
    def get_by_kode(cls,data):
        return DBSession.query(cls).filter(
               and_(
                  cls.kd_kanwil==data['kd_kanwil'],
                  cls.kd_kantor==data['kd_kantor'],
                  cls.temp_thn_bundel==data['temp_thn_bundel'],
                  cls.temp_no_bundel==data['temp_no_bundel'],
                  cls.temp_urut_bundel==data['temp_urut_bundel'],
               )).first()
        
    @classmethod
    def get_max(cls,data):
        return DBSession.query(
                func.max(cls.temp_urut_bundel).label("urt_max")).filter(
                and_(
                  cls.kd_kanwil==data['kd_kanwil'],
                  cls.kd_kantor==data['kd_kantor'],
                  cls.temp_thn_bundel==data['temp_thn_bundel'],
                  cls.temp_no_bundel==data['temp_no_bundel'],
              )).first()

    
    