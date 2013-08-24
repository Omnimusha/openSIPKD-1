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
    kd_propinsi= '32'
    kd_dati2   = '79'
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
    config.add_route('apps',  '/apps')
    config.add_route('appsgrid',  '/apps/grid')
    
    config.add_route('pbbpos', '/pbbpos')
    config.add_route('pbbm', '/pbbm')
    config.add_route('pbb', '/pbb')
    config.add_route('pbbspop', '/pbb/spop')
    config.add_route('pbbspopc1', '/pbb/spop/c1/{t}/{f}')
    config.add_route('pbbspopc2', '/pbb/spop/c2/{t}/{f}/{n1}/{n2}/{n3}')
    config.add_route('pbblspop', '/pbb/lspop')
    config.add_route('pbbdsp', '/pbb/dsp/{kode}')
    
    config.add_route('pbb_ref_kelurahan', '/pbb/ref/kelurahan/{kode}')
    config.add_route('pbb_ref_kelurahan_c', '/pbb/ref/kelurahan/c/{kode}')
    config.add_route('pbb_ref_kecamatan', '/pbb/ref/kecamatan/{kode}')
    config.add_route('pbb_ref_kecamatan_c', '/pbb/ref/kecamatan/c/{kode}')
    
    config.scan()
    return config.make_wsgi_app()
