from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
#aagusti

class osDSP(Base):
    __tablename__ = 'dat_subjek_pajak'

    subjek_pajak_id = Column(String(30), nullable=False, primary_key=True)
    nm_wp = Column(String(30), default='pemilik')
    subjek_pajak_id = Column(String(30), primary_key=True)
    nm_wp = Column(String(30))
    jalan_wp = Column(String(30))
    blok_kav_no_wp = Column(String(15))
    rw_wp = Column(String(2))
    rt_wp = Column(String(3))
    kelurahan_wp = Column(String(30))
    kota_wp = Column(String(30))
    kd_pos_wp = Column(String(5))
    telp_wp = Column(String(20))
    npwp = Column(String(15))
    status_pekerjaan_wp = Column(String(1), default='0')
    kecamatan_wp = Column(String(30))
    propinsi_wp = Column(String(30))

    def __init__(self):
        pass

    """
    def __init__(self,data):
        self.subjek_pajak_id=data['subjek_pajak_id'],
        self.nm_wp=data['nm_wp'],
        self.jalan_wp=data['jalan_wp'],
        self.blok_kav_no_wp=data['blok_kav_no_wp'],
        self.rw_wp=data['rw_wp'],
        self.rt_wp=data['rt_wp'],
        self.kelurahan_wp=data['kelurahan_wp'],
        self.kota_wp=data['kota_wp'],
        self.kd_pos_wp=data['kd_pos_wp'],
        self.telp_wp=data['telp_wp'],
        self.npwp=data['npwp'],
        self.status_pekerjaan_wp=data['status_pekerjaan_wp'],
        self.kecamatan_wp=data['kecamatan_wp'],
        self.propinsi_wp=data['propinsi_wp'],
    """
      
    @classmethod
    def row2dict(cls, row):
        d = {}
        if row:
            for column in row.__table__.columns:
                d[column.name] = getattr(row, column.name)
        return d

    @classmethod
    def get_rows(cls):
        return DBSession.query(cls).all()
       
    @classmethod
    def get_by_nama(cls,nama):
        return DBSession.query(cls).filter(cls.nama==nama).first()
    
    @classmethod
    def get_by_kode(cls,id):
        return DBSession.query(cls).filter( and_(
                cls.subjek_pajak_id==id)
                ).first()        
                
    @classmethod
    def tambah(cls, data):
        DBSession.add(cls(data))
            
    @classmethod
    def edit(cls, data):
        DBSession.merge(cls(data))
            
    @classmethod
    def hapus(cls,data):
        DBSession.query(cls).filter(
            cls.subjek_pajak_id==data.subjek_pajak_id,).delete()
