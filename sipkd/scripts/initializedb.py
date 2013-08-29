import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models.model import (
    DBSession,
    Base,
    osSipkdModel,
    )

from ..models.users import (
    osUsers,
    osGroups,
    osUserGroups
    )
from ..models.apps import  (osApps, osModules)

from ..models.pbb.data.dat_objek_pajak import osDOP
from ..models.pbb.data.dat_subjek_pajak import osDSP

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        """model = osSipkdModel(nama='one', kode='1')
        DBSession.add(model)
        
        model = osUsers(kode='sa', passwd='sa',  nama='sa', locked=0)
        DBSession.add(model)
       
        model = osApps(kode='pbbm', nama='Monitoring PBB', locked=0)
        DBSession.add(model)
        
        model = osApps(kode='admin', nama='ADMIN', locked=0)
        DBSession.add(model)
        
        model = osApps(kode='pbbd', nama='Pendataan PBB', locked=0)
        DBSession.add(model)
        
        model = osModules(kode='data', nama='Pendataan', locked=0, parent='pbbd')
        DBSession.add(model)
        """
        
