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
#from sipkd.models.apbd.user_apbd import osApbdUser

class ApbdViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session=request.session
        if 'logged' not in self.session:
           HTTPFound(location='/logout')
        
        renderer = get_renderer("../../templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        
        renderer = get_renderer("../../templates/main.pt")
        self.main = renderer.implementation().macros['main']

        renderer = get_renderer("../../templates/apbd/nav.pt")
        self.nav = renderer.implementation().macros['nav']
        
    @view_config(route_name='apbd',
                 renderer='../../templates/apbd/home.pt')
    def apbd(self):
        request = self.request
        session = request.session
        resource = None
        url=request.resource_url(resource)

        session['module']='apbd'
        datas=sipkd_init(self.request, self.context)
        
        return dict(datas=datas,
                    url = url)
   
 