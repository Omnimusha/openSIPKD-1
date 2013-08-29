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
from sipkd.models.pbb.pbb import osPbb
from sipkd.models.pbb.ref.kecamatan import osKecamatan

from sipkd.views.views import *


class osfKecamatanValid(colander.MappingSchema):
    kd_kecamatan = colander.SchemaNode(colander.String())
    nm_kecamatan = colander.SchemaNode(colander.String())
    
class osfKecamatan(object):
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
            return { 'form_visible': 0,'kd_propinsi' :gkd_propinsi, 'kd_dati2' : gkd_dati2, 
                  'kd_kecamatan':'', 'nm_kecamatan':'',}
        
# frm action
    @view_config(route_name='pbb_ref_kecamatan',
                 renderer='../../../templates/pbb/ref/kecamatan.pt')
    def pbb_ref_kecamatan(self):
        session = self.request.session
        request = self.request
        resource = None
        url=request.resource_url(resource)
        datas = sipkd_init(self.request, self.context)
        
        datas.update(self.BlankRow())

        fields = self.request.matchdict
        if len(fields['kode'])>5:
            kode=osKecamatan.kode_split(fields['kode']);
            datas.update(osKecamatan.row2dict(osKecamatan.get_by_kode(kode)))
        
        schema = osfKecamatanValid()
        myform = Form(schema, buttons=('submit',))
        if 'btn_save' in self.request.POST:
            controls = self.request.POST.items()
            data2=dict((x, y) for x, y in controls)
            datas.update(data2)
            #datas['message']='Berhasil'
            try:
                appstruct = myform.validate(controls)
                datas.update(appstruct)
                osKecamatan.edit(datas)
            except ValidationFailure, e:
                return dict(datas=datas)
        
            data2=self.BlankRow()
            datas.update(data2)
        return dict(datas=datas)

#    config.add_route('pbb_ref_Kecamatanc', '/pbb/ref/Kecamatan/c/{kode}')
    @view_config(route_name='pbb_ref_kecamatan_c',
                 renderer='json')
    def pbb_ref_kecamatan_c(self):
        fields = self.request.matchdict
        kode = osKecamatan.kode_split(fields['kode'])
        datas={}
        datas['found'] = 0
        if kode:
            d=osKecamatan.row2dict(osKecamatan.get_by_kode(kode))
            if d: 
                datas['found'] = 1
                datas.update(d)
        return json.dumps(datas, default=osPbb.default)

        