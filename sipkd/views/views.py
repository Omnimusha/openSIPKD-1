from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models.model import (
    DBSession,
    #osApp,
    )

from sipkd.models.apps import osApps

def sipkd_init(request):
    datas={}
    if 'logged' in request.session:
        print 'username', request.session['usernm']
        datas['usernm']=request.session['usernm'], 
        if request.session['sa']==1:
            datas['opts']=osApps.get_rows()
            opts = osApps.get_rows()
        else:
            opts = ()
    else:
        datas['usernm']=''
    datas['title']="OpenSIPKD"
    datas['message']="Silahkan Isi Form di bawah ini"
    
    return datas

@view_config(route_name='home1', renderer='../templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'sipkd'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sipkd_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

