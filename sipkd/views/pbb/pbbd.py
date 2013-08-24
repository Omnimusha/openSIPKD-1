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

class PbbViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
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

        datas=sipkd_init(self.request)

        return dict(datas=datas)
   
    @view_config(route_name='pbblspop',
                 renderer='../../templates/pbb/lspop.pt')
    def pbblspop(self):
 
  
        return dict(datas=datas)
