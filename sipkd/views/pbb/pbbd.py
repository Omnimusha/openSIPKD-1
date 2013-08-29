from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import has_permission
from sqlalchemy import *
from sipkd.models import *
from sipkd.models.model import *
from sqlalchemy.exc import DBAPIError
import json
import types
from sipkd.models.apps import osApps
from sipkd.views.views import *
from data.spops import osSpop
from sipkd.models.pbb.user_pbb import osPbbUser
class PbbViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session=request.session
        if 'logged' not in self.session:
           HTTPFound(location='/logout')
        
        data=osPbbUser.get_by_user_id(self.session['user_id'])
        if data:
            self.session['kd_kanwil']=data.kd_kanwil
            self.session['kd_kantor']=data.kd_kantor
            #session['kd_kppbb'] =data.kd_kppbb
            #session['kd_bank_tunggal']=data.kd_bank_tunggal
            #session['kd_bank_persepsi']=data.kd_bank_persepsi
        else:
            if self.session['userid']=='sa':
                self.session['kd_kanwil']='09'
                self.session['kd_kantor']='19'
            else:
                HTTPFound(location='/logout')
            
        renderer = get_renderer("../../templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        
        renderer = get_renderer("../../templates/main.pt")
        self.main = renderer.implementation().macros['main']

        renderer = get_renderer("../../templates/pbb/nav.pt")
        self.nav = renderer.implementation().macros['nav']
        
    @view_config(route_name='pbb',
                 renderer='../../templates/pbb/home.pt')
    def pbb(self):
        from sipkd.models.apps import osApps
        session = self.request.session
        request = self.request
        resource = None

        url=request.resource_url(resource)

        session['module']='pbb'
        datas=sipkd_init(self.request, self.context)
        
        return dict(datas=datas)
   
 