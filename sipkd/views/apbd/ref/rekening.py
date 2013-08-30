import sys
import json
import types
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import has_permission

from sqlalchemy import *
from sqlalchemy.exc import DBAPIError

import colander
from deform import Form
from deform import ValidationFailure

from sipkd.models.model import *
from sipkd.models.apbd.ref.rekening import osRefRekening

from sipkd.views.views import *


class osfRekeningValid(colander.MappingSchema):
    kd_kecamatan = colander.SchemaNode(colander.String())
    kd_kelurahan = colander.SchemaNode(colander.String())
    nm_kelurahan = colander.SchemaNode(colander.String())
    kd_sektor    = colander.SchemaNode(colander.String(),
                   missing = '01')
    no_kelurahan = colander.SchemaNode(
                   colander.Integer(),
                    missing = None,)    
    
class osfRekening(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        renderer = get_renderer("../../../templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        
        renderer = get_renderer("../../../templates/main.pt")
        self.main = renderer.implementation().macros['main']

        renderer = get_renderer("../../../templates/pbb/nav.pt")
        self.nav = renderer.implementation().macros['nav']
                
    @classmethod
    def BlankRow(cls):
            return {'form_visible':0,
                    'id' : '',
                    'kode' : '',
                    'nama' : '',
                    'level_id' : '',
                    'defsign' : '',
                    'header_id' : '',
                    'locked' : '',
                  }
#init
    @view_config(route_name='apbd_ref1',
                 renderer='../../../templates/apbd/ref/rekening.pt')
    def apbd_ref1(self):
        request = self.request
        session = request.session
        resource = None
        url=request.resource_url(resource)
        datas=sipkd_init(self.request, self.context)

        if session['logged']<>1:
           return HTTPFound(location='/logout') 
  
        return dict(datas=datas, url=url)
#grid
    @view_config(route_name='apbd_ref1_grid', renderer='json')
    def apbd_ref1_grid(self):
        resource = None
               
        grids={"aaData":[]}
        
        for opt in opts: 
            checked = opt.locked==1 and "checked" or ""
            grids['aaData'].append([opt.id, opt.kode, opt.nama, opt.defsign,
            '<input type="checkbox" onchange="update_stat(%d,this.checked);" name="disabled" disabled %s>' % (opt.id,checked)
            
            ])
        return grids
        
# form
    @view_config(route_name='apbd_ref1_form',
                 renderer='../../../templates/apbd/ref/rekening_form.pt')
    def apbd_ref1_form(self):
        request = self.request
        session = request.session
        resource = None
        url=request.resource_url(resource)
        datas=sipkd_init(self.request, self.context)
        datas.update(self.BlankRow())

        if session['logged']<>1:
           return HTTPFound(location='/logout') 
        
        fields = self.request.matchdict
        datas.update(self.BlankRow())
        if 'id' in fields:
            datas['form_visible'] = 1
            datas['id']=fields['id']
            datas.update(osRefRekening.row2dict(osRefRekening.get_by_id(datas)))

        schema = osfRekeningValid()
        myform = Form(schema, buttons=('submit',))
        if 'btn_save' in self.request.POST:
            controls = self.request.POST.items()
            data2=dict((x, y) for x, y in controls)
            datas.update(data2)
            #datas['message']='Berhasil'
            try:
                appstruct = myform.validate(controls)
                datas.update(appstruct)
                osKelurahan.edit(datas)
            except ValidationFailure, e:
                return dict(datas=datas)
        
            data2=self.BlankRow()
            datas.update(data2)
            #return dict(datas=datas)
        return dict(datas=datas, url=url)

#cek kode
    @view_config(route_name='apbd_ref1_cek',
                 renderer='json')
    def apbd_ref1_cek(self):
        fields = self.request.matchdict
        datas={}
        datas['found'] = 0
        kode = fields['kode']
        if kode:
            d=osKelurahan.row2dict(osRefRekening.get_by_kode(kode))
            if d: 
                datas['found'] = 1
                datas.update(d)
        return json.dumps(datas, default=json_format)

        