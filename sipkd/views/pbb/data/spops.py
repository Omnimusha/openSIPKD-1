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

from sipkd.models import *
from sipkd.models.model import *
from sipkd.models.apps import osApps
from sipkd.models.pbb.pbb import osPbb
from sipkd.models.pbb.data import *
from sipkd.models.pbb.data.dat_objek_pajak import osDOP
from sipkd.models.pbb.data.dat_subjek_pajak import osDSP
from sipkd.models.pbb.data.dat_op_bumi import osDOPBumi
from sipkd.models.pbb.ref.lookup import osLookup

from sipkd.views.views import *


class osSpopValid(colander.MappingSchema):
    pass
    """name = colander.SchemaNode(colander.String())
    shoe_size = colander.SchemaNode(
        colander.Integer(),
        missing = 0,
    )"""
    
    
class osSpop(object):
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
            return { 'form_visible': '0',  
                  'frmjns':'S', 'frmjnstxt':'SPOP',  'frm1':'', 'frm2':'', 'frm3':'',
                  'kec2':'', 'kel2':'', 'blk2':'', 'urt2':'', 'jns2':'',
                  'kec3':'', 'kel3':'', 'blk3':'', 'urt3':'', 'jns3':'',
                  'kd_propinsi' :gkd_propinsi, 'kd_dati2' : gkd_dati2, 
                  'kd_kecamatan':'', 'kd_kelurahan':'',
                  'kd_blok':'', 'no_urut':'', 'kd_jns_op':'', 'subjek_pajak_id':'',
                  'no_formulir_spop':'', 'no_persil':'', 'jalan_op':'',
                  'blok_kav_no_op':'', 'rw_op':'', 'rt_op':'', 'kd_status_cabang':0,
                  'kd_status_wp':'', 'total_luas_bumi':0, 'total_luas_bng':0,
                  'njop_bumi':0, 'njop_bng':0,  'status_peta_op':0, 'jns_transaksi_op':0,
                  'tgl_pendataan_op':'', 'nip_pendata':'', 'tgl_pemeriksaan_op':'',
                  'nip_pemeriksa_op':'', 'tgl_perekaman_op':'', 'nip_perekam_op':'',
                  'no_bumi':'', 'kd_znt':'', 'luas_bumi':'', 'jns_bumi':'', 'nilai_sistem_bumi':0,
                  'nm_wp':'', 'jalan_wp':'', 'blok_kav_no_wp':'', 'rw_wp':'',
                  'rt_wp':'', 'kelurahan_wp':'', 'kota_wp':'', 'kd_pos_wp':'','telp_wp':'', 
                  'npwp':'', 'status_pekerjaan_wp':'', 'kecamatan_wp':'','propinsi_wp':'',
                  }

                  
    def validate(cls):
        pass
        
    def get_row(self):
        session = self.request.session
        request = self.request
        fields = request.matchdict
        frm = osPbb.frm_split(fields['f'])
        if frm:
            datas=osDOP.row2dict(osDOP.get_by_form(frm))

        if 'n' in fields:
            nop = osPbb.frm_split(fields['n'])
            if not datas and nop:
                datas=osDOP.row2dict(osDOP.get_by_kode(nop))
            
        if datas:
            data2=osDOPBumi.row2dict(osDOPBumi.get_by_kode(datas))
            datas.update(data2)
            data2=osDSP.row2dict(osDSP.get_by_kode(datas['subjek_pajak_id']))
            datas.update(data2)
            datas['found'] = 1
        else:
            datas=osSpop.BlankRow()
            datas['found'] = 0
            
        row=osDOP.frm_max(frm)
        print row[0]
        if row:
            datas['frm_max']=row[0]
        else:    
            datas['frm_max']=''.join((frm['tahun'],frm['bundle'],'000'))
        if abs(float(datas['frm_max'])-float(osPbb.frm_join(frm)))>1:
            datas['frm_fail']=1
        else:
            datas['frm_fail']=0
        return datas
        
# frm action
    @view_config(route_name='pbb_spop',
                 renderer='../../../templates/pbb/spop.pt')
    def pbbspop(self):
        session = self.request.session
        #if session['logged']<>1:
        #   return HTTPFound(location='/logout') 

        request = self.request
        
        resource = None
        url=request.resource_url(resource)
        datas = sipkd_init(request, self.context)
        datas.update(osSpop.BlankRow())
        datas['wp_pekerjaan']=osLookup.get_wp_pekerjaan()
        datas['wp_status']=osLookup.get_wp_status()

        if self.request.session['sa']==1:
            datas['opts']=osApps.get_rows()
            opts = osApps.get_rows()
        else:
            pass

        schema = osSpopValid()
        myform = Form(schema, buttons=('submit',))
        if 'btn_save' in self.request.POST:
            controls = self.request.POST.items()
            data2=dict((x, y) for x, y in controls)
            datas.update(data2)
            datas['form_visible']= '1'
            datas['readonly'] = 'readonly'
            try:
                appstruct = myform.validate(controls)
            except ValidationFailure, e:
                return dict(title="OpenSIPKD",
                    message="",
                    usernm=self.request.session['usernm'], 
                    opts=opts,
                    datas=datas,
                    url=url)

            # Process the valid form data, do some work
            #try:
            if osDSP.get_by_kode(datas['subjek_pajak_id']):
                osDSP.edit(datas)
            else:
                osDSP.tambah(datas)
                
            if datas['jns_transaksi_op']==1:
                osDOP.tambah(data)
                osDOPBumi.tambah(data)
            elif datas['jns_transaksi_op']==4:
                osDOP.hapus_nop_bersama(data)
            else: 
                osDOP.edit(datas)
                osDOPBumi.edit(datas)
                
                #DBSession.commit()
            #except: 
            #    print "Unexpected error:", sys.exc_info()[0]
            return dict(title="OpenSIPKD",
                message="",
                usernm=self.request.session['usernm'], 
                opts=opts,
                datas=datas,
                url=url)
                    
            data2=cls.BlankRow()
            datas.update(data2)
            datas['form_visible']= '0'
            datas['readonly'] = ''
            return dict(datas=datas,
                url=url)
        return dict(title="OpenSIPKD",
                    message="",
                    usernm=self.request.session['usernm'], 
                    opts=opts,
                    datas=datas,
                    url=url)
#frm keypress                    
    @view_config(route_name='pbb_spop_c1',
                 renderer='json')
    def pbbspopc1(self):
        datas=self.get_row()
        return json.dumps(datas, default=osPbb.default)

# button validate        
    @view_config(route_name='pbb_spop_c2',
                 renderer='json')
    def pbbspopc2(self):
        datas=self.get_row()
        return json.dumps(datas, default=osPbb.default)
# cari wp
    @view_config(route_name='pbb_dsp',
                 renderer='json')
    def pbbdsp(self): 
        session = self.request.session
        #if session['logged']<>1:
        #   return HTTPFound(location='/logout') 

        request = self.request
        fields = request.matchdict
        
        datas=osDSP.row2dict(osDSP.get_by_kode(fields['kode']))
        if datas:
            datas['found'] = 1
        else:
            datas['found'] = 0
        return json.dumps(datas, 
                          default = osPbb.default)
        

        