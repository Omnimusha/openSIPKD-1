from types import *
from datetime import datetime, date

class osPbb(object):
    def __init__(self):
      pass
      
    @classmethod
    def nop_split(cls, kode):
        return {'kd_propinsi':kode[0:2], 'kd_dati2':kode[2:4], 'kd_kecamatan':kode[4:7], 'kd_kelurahan':kode[7:10], 
                'kd_blok': kode[10:13], 'no_urut':kode[13:17], 'kd_jns_op':kode[17:18]}
        
    @classmethod
    def nop_join(cls, kode):
        return ''.join( (kode['kd_propinsi'], kode['kd_dati2'], kode['kd_kecamatan'], kode['kd_kelurahan'], 
                        kode['kd_blok'], kode['no_urut'], kode['kd_jns_op']))  
        
    @classmethod
    def nop_join_format(cls, kode):
        return ''.join( (kode['kd_propinsi'], '.', kode['kd_dati2'], '-', kode['kd_kecamatan'], '.', kode['kd_kelurahan'], 
                        '-', kode['kd_blok'], kode['no_urut'], kode['kd_jns_op']))  

    @classmethod
    def frm_split(cls, kode):
        return {'tahun':kode[0:4], 'bundle':kode[4:8], 'no_urut':kode[8:11]}
        
    @classmethod
    def frm_join(cls, kode):
        return ''.join((kode['tahun'],kode['bundle'],kode['no_urut']))

    @classmethod
    def default(cls,o):
        if type(o) is date:
            return o.strftime("%d-%m-%Y")