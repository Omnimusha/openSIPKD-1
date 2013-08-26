from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types
class osDOPBng(Base):
    __tablename__ = 'dat_op_bangunan'
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(3), primary_key=True)
    kd_kelurahan = Column(String(3), primary_key=True)
    kd_blok = Column(String(3), primary_key=True)
    no_urut = Column(String(4), primary_key=True)
    kd_jns_op = Column(String(1), primary_key=True)
    no_bng = Column(Float, primary_key=True)
    kd_jpb = Column(String(2))
    no_formulir_lspop = Column(String(11))
    thn_dibangun_bng = Column(String(4))
    thn_renovasi_bng = Column(String(4))
    luas_bng = Column(Float)
    jml_lantai_bng = Column(Float)
    kondisi_bng = Column(String(1))
    jns_konstruksi_bng = Column(String(1))
    jns_atap_bng = Column(String(1))
    kd_dinding = Column(String(1))
    kd_lantai = Column(String(1))
    kd_langit_langit = Column(String(1))
    nilai_sistem_bng = Column(Float)
    jns_transaksi_bng = Column(String(1))
    tgl_pendataan_bng = Column(DateTime)
    nip_pendata_bng = Column(String(18))
    tgl_pemeriksaan_bng = Column(DateTime)
    nip_pemeriksa_bng = Column(String(18))
    tgl_perekaman_bng = Column(DateTime)
    nip_perekam_bng = Column(String(18))

    def __init__(self,data):
        self.kd_propinsi=data['kd_propinsi'],
        self.kd_dati2=data['kd_dati2'],
        self.kd_kecamatan=data['kd_kecamatan'],
        self.kd_kelurahan=data['kd_kelurahan'],
        self.kd_blok=data['kd_blok'],
        self.no_urut=data['no_urut'],
        self.kd_jns_op=data['kd_jns_op'],
        self.no_bng=data['no_bng'],
        self.kd_jpb=data['kd_jpb'],
        self.no_formulir_lspop=data['no_formulir_lspop'],
        self.thn_dibangun_bng=data['thn_dibangun_bng'],
        self.thn_renovasi_bng=data['thn_renovasi_bng'],
        self.luas_bng=data['luas_bng'],
        self.jml_lantai_bng=data['jml_lantai_bng'],
        self.kondisi_bng=data['kondisi_bng'],
        self.jns_konstruksi_bng=data['jns_konstruksi_bng'],
        self.jns_atap_bng=data['jns_atap_bng'],
        self.kd_dinding=data['kd_dinding'],
        self.kd_lantai=data['kd_lantai'],
        self.kd_langit_langit=data['kd_langit_langit'],
        self.nilai_sistem_bng=data['nilai_sistem_bng'],
        self.jns_transaksi_bng=data['jns_transaksi_bng'],
        self.tgl_pendataan_bng=data['tgl_pendataan_bng'],
        self.nip_pendata_bng=data['nip_pendata_bng'],
        self.tgl_pemeriksaan_bng=data['tgl_pemeriksaan_bng'],
        self.nip_pemeriksa_bng=data['nip_pemeriksa_bng'],
        self.tgl_perekaman_bng=data['tgl_perekaman_bng'],
        self.nip_perekam_bng=data['nip_perekam_bng'],

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
                cls.no_bng==kode['no_bng'],
              )).first()        

    @classmethod
    def get_by_form(cls,frm):
        return DBSession.query(cls).filter( 
                cls.no_formulir_lspop==osPbb.frm_join(frm)
                ).first()     
                
    @classmethod
    def tambah(cls, datas):
        data=cls(datas)
        DBSession.add(cls(data))
            
    @classmethod
    def edit(cls, data):
        DBsession.merge(cls(data))
            
    @classmethod
    def hapus(cls,datas,kode):
        DBSession.query(cls).filter( and_( cls.kd_propinsi==kode['kd_propinsi'],
                cls.kd_dati2==kode['kd_dati2'],
                cls.kd_kecamatan==kode['kd_kecamatan'],
                cls.kd_kelurahan==kode['kd_kelurahan'],
                cls.kd_blok==kode['kd_blok'],
                cls.no_urut==kode['no_urut'],
                cls.kd_jns_op==kode['kd_jns_op'],
                cls.no_bng==kode['no_bng'],
              )).delete()

