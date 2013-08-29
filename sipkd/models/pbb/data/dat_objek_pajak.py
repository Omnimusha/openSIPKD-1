from datetime import datetime

from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types

class osDOP(Base):
    __tablename__ = 'dat_objek_pajak'
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(3), primary_key=True)
    kd_kelurahan = Column(String(3), primary_key=True)
    kd_blok = Column(String(3), primary_key=True)
    no_urut = Column(String(4), primary_key=True)
    kd_jns_op = Column(String(1), primary_key=True)
    subjek_pajak_id = Column(String(30))
    no_formulir_spop = Column(String(11))
    no_persil = Column(String(5))
    jalan_op = Column(String(30))
    blok_kav_no_op = Column(String(15))
    rw_op = Column(String(2))
    rt_op = Column(String(3))
    kd_status_cabang = Column(Float)
    kd_status_wp = Column(String(1))
    total_luas_bumi = Column(Float)
    total_luas_bng = Column(Float)
    njop_bumi = Column(Float)
    njop_bng = Column(Float)
    status_peta_op = Column(Float)
    jns_transaksi_op = Column(String(1))
    tgl_pendataan_op = Column(DateTime)
    nip_pendata = Column(String(18))
    tgl_pemeriksaan_op = Column(DateTime)
    nip_pemeriksa_op = Column(String(18))
    tgl_perekaman_op = Column(DateTime)
    nip_perekam_op = Column(String(18))
   
    def __init__(self, data):
        self.kd_propinsi=data['kd_propinsi'],
        self.kd_dati2=data['kd_dati2'],
        self.kd_kecamatan=data['kd_kecamatan'],
        self.kd_kelurahan=data['kd_kelurahan'],
        self.kd_blok=data['kd_blok'],
        self.no_urut=data['no_urut'],
        self.kd_jns_op=data['kd_jns_op'],
        self.subjek_pajak_id=data['subjek_pajak_id'],
        self.no_formulir_spop=data['no_formulir_spop'],
        self.no_persil=data['no_persil'],
        self.jalan_op=data['jalan_op'],
        self.blok_kav_no_op=data['blok_kav_no_op'],
        self.rw_op=data['rw_op'],
        self.rt_op=data['rt_op'],
        self.kd_status_cabang=data['kd_status_cabang'],
        self.kd_status_wp=data['kd_status_wp'],
        self.total_luas_bumi=data['total_luas_bumi'],
        self.total_luas_bng=data['total_luas_bng'],
        self.njop_bumi=data['njop_bumi'],
        self.njop_bng=data['njop_bng'],
        self.status_peta_op=data['status_peta_op'],
        self.jns_transaksi_op=data['jns_transaksi_op'],
        self.tgl_pendataan_op=datetime.strptime(data['tgl_pendataan_op'],'%d-%m-%Y'),
        self.nip_pendata=data['nip_pendata'],
        self.tgl_pemeriksaan_op=datetime.strptime(data['tgl_pemeriksaan_op'],'%d-%m-%Y'),
        self.nip_pemeriksa_op=data['nip_pemeriksa_op'],
        self.tgl_perekaman_op=datetime.now(),
        self.nip_perekam_op=data['nip_perekam_op'],

      
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
                cls.kd_jns_op==kode['kd_jns_op'],)
                ).first()        

    @classmethod
    def get_by_form(cls,frm):
        return DBSession.query(cls).filter( 
                cls.no_formulir_spop==osPbb.frm_join(frm)
                ).first()     
    
    @classmethod
    def tambah(cls, data):
        DBSession.add(cls(data))
            
    @classmethod
    def edit(cls, data):
        DBSession.merge(osDOP(data))
            
    @classmethod
    def hapus(cls,nop):
        DBSession.query(cls).filter( and_(
                cls.kd_propinsi==nop.kd_propinsi ,
                cls.kd_dati2==nop.kd_dati2 ,
                cls.kd_kecamatan==nop.kd_kecamatan ,
                cls.kd_kelurahan==nop.kd_kelurahan ,
                cls.kd_blok==nop.kd_blok ,
                cls.no_urut==nop.no_urut ,
                cls.kd_jns_op==nop.kd_jns_op)
                ).delete()
    
 