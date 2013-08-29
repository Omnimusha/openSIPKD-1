from sipkd.models.model import * 
from sqlalchemy import and_
from sipkd.models.pbb.pbb import osPbb
import types


class osDSP(Base):
    __tablename__ = 'dat_subjek_pajak'

    subjek_pajak_id = Column(String(30), nullable=False, primary_key=True)
    nm_wp = Column(String(30), default='pemilik')
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
    def get_by_id(cls,id):
        return DBSession.query(cls).filter(cls.id==id).first()
        
    @classmethod
    def get_by_nama(cls,nama):
        return DBSession.query(cls).filter(cls.nama==nama).first()
    
    @classmethod
    def get_by_kode(cls,id):
        return DBSession.query(cls).filter( and_(
                cls.subjek_pajak_id==id)
                ).first()        

    @classmethod
    def tambah(cls, datas):
        data=cls(datas)
        DBSession.add(
        
        )
            
    @classmethod
    def edit(cls, data):
        DBsession.merge(kd_propinsi==datas.kd_propinsi ,
            kd_dati2==datas.kd_dati2 ,
            kd_kecamatan==datas.kd_kecamatan ,
            kd_kelurahan==datas.kd_kelurahan ,
            kd_blok==datas.kd_blok ,
            no_urut==datas.no_urut ,
            kd_jns_op==datas.kd_jns_op ,
            subjek_pajak_id==datas.subjek_pajak_id ,
            no_formulir_spop==datas.no_formulir_spop ,
            no_persil==datas.no_persil ,
            jalan_op==datas.jalan_op ,
            blok_kav_no_op==datas.blok_kav_no_op ,
            rw_op==datas.rw_op ,
            rt_op==datas.rt_op ,
            kd_status_cabang==datas.kd_status_cabang ,
            kd_status_wp==datas.kd_status_wp ,
            total_luas_bumi==datas.total_luas_bumi ,
            total_luas_bng==datas.total_luas_bng ,
            njop_bumi==datas.njop_bumi ,
            njop_bng==datas.njop_bng ,
            status_peta_op==datas.status_peta_op ,
            jns_transaksi_op==datas.jns_transaksi_op ,
            tgl_pendataan_op==datas.tgl_pendataan_op ,
            nip_pendata==datas.nip_pendata ,
            tgl_pemeriksaan_op==datas.tgl_pemeriksaan_op ,
            nip_pemeriksa_op==datas.nip_pemeriksa_op ,
            tgl_perekaman_op==datas.tgl_perekaman_op ,
            nip_perekam_op==datas.nip_perekam_op)
            
    @classmethod
    def hapus(cls,datas,nop):
        DBSession.query(cls).filter( and_(
                cls.kd_propinsi==nop.kd_propinsi ,
                cls.kd_dati2==nop.kd_dati2 ,
                cls.kd_kecamatan==nop.kd_kecamatan ,
                cls.kd_kelurahan==nop.kd_kelurahan ,
                cls.kd_blok==nop.kd_blok ,
                cls.no_urut==nop.no_urut ,
                cls.kd_jns_op==nop.kd_jns_op)
                ).delete()

