from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.renderers import JSON

from models.model import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings, session_factory=my_session_factory)

    config.add_renderer('json', JSON(indent=0))    
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route('home', '/')
    config.add_route('main', '/main')
    config.add_route('home1', '/home1')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('admin', '/admin')
    config.add_route('admin_apps',  '/admin/apps')
    config.add_route('admin_apps_grid', '/admin/apps/grid')
    config.add_route('admin_apps_update_stat',  '/admin/apps/update_stat/{id}/{value}')
    config.add_route('rka', '/rka')
    config.add_route('spp', '/spp')
    config.add_route('spm', '/spm')
    config.add_route('sp2d', '/sp2d')
    config.add_route('pad', '/pad')
    
    
    config.add_route('pbb_pos', '/pbbpos')
    config.add_route('pbb_m', '/pbbm')
    
    config.add_route('pbb', '/pbb')
    config.add_route('pbb_spop', '/pbb/spop')
    config.add_route('pbb_spop_c1', '/pbb/spop/c1/{t}/{f}')
    config.add_route('pbb_spop_c2', '/pbb/spop/c2/{t}/{f}/{n1}/{n2}/{n3}')
    config.add_route('pbb_dsp', '/pbb/dsp/{kode}')
    
    config.add_route('pbb_lspop', '/pbb/lspop')
    config.add_route('pbb_lspop_c1', '/pbb/lspop/c/{t}/{f}/{n1}')
    
    config.add_route('pbb_ref_kelurahan', '/pbb/ref/kelurahan/{kode}')
    config.add_route('pbb_ref_kelurahan_c', '/pbb/ref/kelurahan/c/{kode}')
    config.add_route('pbb_ref_kecamatan', '/pbb/ref/kecamatan/{kode}')
    config.add_route('pbb_ref_kecamatan_c', '/pbb/ref/kecamatan/c/{kode}')
    
    config.add_route('apbd',      '/apbd')        #Home APBD apbd.py 
    config.add_route('apbd_conf', '/apbd/config') #Configurasi Tahun Anggaran apbd_conf.py
    config.add_route('apbd_ref1', '/apbd/ref1') #Rekening
    config.add_route('apbd_ref1_grid', '/apbd/ref1/grid')
    config.add_route('apbd_ref1_form', '/apbd/ref1/form/{id}')
    config.add_route('apbd_ref1_cek', '/apbd/ref1/cek/{kode}')
    
    config.add_route('apbd_ref2', '/apbd/ref2') #Urusan
    config.add_route('apbd_ref3', '/apbd/ref3') #Program
    config.add_route('apbd_ref4', '/apbd/ref4') #Kegiatan
    config.add_route('apbd_ref5', '/apbd/ref5') #Unit Kerjna
    config.add_route('apbd_ref6', '/apbd/ref6') #Fungsi
    
    config.add_route('apbd_rka1', '/apbd/rka1') #pendapatan
    config.add_route('apbd_rka2', '/apbd/rka2') #belanja
    config.add_route('apbd_rka3', '/apbd/rka3') #pembiayaan penerimaan
    config.add_route('apbd_rka4', '/apbd/rka4') #pembiayaan pengeluaran
    
    config.add_route('apbd_tu1',  '/apbd/tu1')      #TBP
    config.add_route('apbd_tu11', '/apbd/tu11')     #TBP Lap
    config.add_route('apbd_tu2',  '/apbd/tu2')      #STS
    config.add_route('apbd_tu21', '/apbd/tu21')     #STS LAP
    config.add_route('apbd_tu3',  '/apbd/tu3')      #SPP
    config.add_route('apbd_tu31', '/apbd/tu31')     #SPP_LAP
    config.add_route('apbd_tu4',  '/apbd/tu4')      #SPM
    config.add_route('apbd_tu41', '/apbd/tu41')     #SPM_LAP
    config.add_route('apbd_tu5',  '/apbd/tu5')      #SP2D
    config.add_route('apbd_tu51', '/apbd/tu51')     #SP2D_LAP
    config.add_route('apbd_tu6',  '/apbd/tu6')      #SPJ
    config.add_route('apbd_tu61', '/apbd/tu61')     #SPJ LAP

    config.add_route('apbd_acc1',  '/apbd/acc1')      #Journal
    config.add_route('apbd_acc2',  '/apbd/acc11')     #Journal_LAP
    
    config.scan()
    return config.make_wsgi_app()
