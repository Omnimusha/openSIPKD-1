from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import has_permission
#from sqlalchemy import *
#from sipkd.models import *
from sqlalchemy.exc import DBAPIError
import json
from sipkd.views.views import sipkd_init

class AdminViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        renderer = get_renderer("../templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        
        renderer = get_renderer("../templates/main.pt")
        self.main = renderer.implementation().macros['main']

        renderer = get_renderer("../templates/admin/nav.pt")
        self.nav = renderer.implementation().macros['nav']
        
    @view_config(route_name='admin',
                 renderer='../templates/admin/home.pt')
    def admin(self):
        from sipkd.models.apps import osApps
        session = self.request.session
        request = self.request
        session['module']='admin'
        resource = None
        datas=sipkd_init(self.request, self.context)
        if session['logged']<>1:
           return HTTPFound(location='/logout') 
        opts=[dict(nama='ADMIN', kode='admin')]
        url=request.resource_url(resource)
        #url='a'
        if self.request.session['sa']==1:
            opts = osApps.get_rows()
            print opts
        else:
            pass
        return dict(datas=datas, url=url)
                    
    @view_config(route_name = 'admin_apps',
                 renderer   = '../templates/admin/apps.pt')
    def apps(self):
        from ..models.apps import osApps
        session = self.request.session
        request = self.request
        datas=sipkd_init(self.request, self.context)
        resource = None
        if session['logged']<>1:
           return HTTPFound(location='/logout') 
        url=request.resource_url(resource)
        if self.request.session['sa']==1:
            opts = osApps.get_rows()
            opts=[dict(nama='ADMIN', kode='admin')]
            print opts
        else:
            pass
  
        return dict(datas=datas, url=url)

    @view_config(route_name='admin_apps_grid', renderer='json')
    def appsgrid(self):
        from ..models.apps import osApps
        resource = None
        opts = osApps.get_rows()
        
        a={"aaData":[]}
        for opt in opts:
            a['aaData']=[opt.id,opt.nama]
            print a
        
        #arow = json.dumps(opts, indent=4)
        #print arow
        
        #for opt in opts:
            
        a= {"aaData":[
            ["1","PBB","pbb","<input type=\"checkbox\" onchange=\"update_stat(1,this.checked);\" name=\"disabled\" checked>"], 
            ["2","BPHTB","bphtb","<input type=\"checkbox\" onchange=\"update_stat(2,this.checked);\" name=\"disabled\" >"], \
            ["3","POSPBB","pospbb","<input type=\"checkbox\" onchange=\"update_stat(3,this.checked);\" name=\"disabled\" >"], \
            ["4","MONITORING PBB","pbbm","<input type=\"checkbox\" onchange=\"update_stat(4,this.checked);\" name=\"disabled\" >"], \
            ["5","ADMIN","admin","<input type=\"checkbox\" onchange=\"update_stat(5,this.checked);\" name=\"disabled\" checked>"], \
            ["6","PBB DATA","pbbdata","<input type=\"checkbox\" onchange=\"update_stat(6,this.checked);\" name=\"disabled\" >"] \
            ]}
        
        return a
                    

