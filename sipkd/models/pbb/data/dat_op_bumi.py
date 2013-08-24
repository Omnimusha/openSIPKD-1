from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
class osDOPBumi(Base):
    __tablename__ = 'dat_op_bumi'
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(3), primary_key=True)
    kd_kelurahan = Column(String(3), primary_key=True)
    kd_blok = Column(String(3), primary_key=True)
    no_urut = Column(String(4), primary_key=True)
    kd_jns_op = Column(String(1), primary_key=True)
    no_bumi = Column(Float, primary_key=True)
    kd_znt = Column(String(2))
    luas_bumi = Column(Float)
    jns_bumi = Column(String(1))
    nilai_sistem_bumi = Column(Float)

    
    def __init__(self, data):
        self.kd_propinsi=data['kd_propinsi'],
        self.kd_dati2=data['kd_dati2'],
        self.kd_kecamatan=data['kd_kecamatan'],
        self.kd_kelurahan=data['kd_kelurahan'],
        self.kd_blok=data['kd_blok'],
        self.no_urut=data['no_urut'],
        self.kd_jns_op=data['kd_jns_op'],
        self.no_bumi=data['no_bumi'] or 1,
        self.kd_znt=data['kd_znt'] or 'AA',
        self.luas_bumi=data['luas_bumi'] or 0,
        self.jns_bumi=data['jns_bumi'] or 0,
        self.nilai_sistem_bumi=data['nilai_sistem_bumi'] or 0,
      
      
    @classmethod
    def row2dict(cls,row):
        d = {}
        if row:
            for column in row.__table__.columns:
                d[column.name] = getattr(row, column.name)
        return d

    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).all()
        
    @classmethod
    def get_by_id(cls,id):
        return DBSession.query(cls).filter(cls.id==id).first()
        
    @classmethod
    def get_by_nama(cls,nama):
        return DBSession.query(cls).filter(cls.nama==nama).first()
    
    @classmethod
    def get_by_kode(cls,kode):
        return DBSession.query(cls).filter( and_(
                cls.kd_propinsi==kode['kd_propinsi'],
                cls.kd_dati2==kode['kd_dati2'],
                cls.kd_kecamatan==kode['kd_kecamatan'],
                cls.kd_kelurahan==kode['kd_kelurahan'],
                cls.kd_blok==kode['kd_blok'],
                cls.no_urut==kode['no_urut'],
                cls.kd_jns_op==kode['kd_jns_op'],
                cls.no_bumi=='01')
                ).first()        

    @classmethod
    def get_by_form(cls,frm):
        return DBSession.query(cls).filter( 
                cls.no_formulir_spop==osPbb.frm_merge(frm)
                ).first()     
                
    @classmethod
    def tambah(cls, data):
        DBSession.add(cls(data))
            
    @classmethod
    def edit(cls, data):
        DBSession.merge(cls(data))
            
    @classmethod
    def hapus(cls,data):
        DBSession.query(cls).filter( and_(
        cls.kd_propinsi==data.kd_propinsi,
        cls.kd_propinsi==data['kd_propinsi'],
        cls.kd_dati2==data['kd_dati2'],
        cls.kd_kecamatan==data['kd_kecamatan'],
        cls.kd_kelurahan==data['kd_kelurahan'],
        cls.kd_blok==data['kd_blok'],
        cls.no_urut==data['no_urut'],
        cls.kd_jns_op==data['kd_jns_op'],
        cls.no_bumi==data['no_bumi'],
        )).delete()

