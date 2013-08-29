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

from sipkd.models.pbb.pbb import osPbb
from sipkd.models.pbb.data.dat_objek_pajak import osDOP
from sipkd.models.pbb.data.dat_op_bng import osDOPBng
from sipkd.models.pbb.ref.lookup import osLookup
from sipkd.models.pbb.tmp.maxbundle import osMaxBundle

from sipkd.views.views import *

class osLSpopValid(colander.MappingSchema):
    pass
    """name = colander.SchemaNode(colander.String())
    shoe_size = colander.SchemaNode(
        colander.Integer(),
        missing = 0,
    )"""
    
    
class osLSpop(object):
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
                  'frmjns':'L', 'frmjnstxt':'LSPOP',  'frm1':'', 'frm2':'', 'frm3':'',
                  'kd_propinsi' :gkd_propinsi, 'kd_dati2' : gkd_dati2, 
                  'kd_kecamatan':'', 'kd_kelurahan':'',
                  'kd_blok':'', 'no_urut':'', 'kd_jns_op':'', 'jns_transaksi_op':1, 
                  
                  }

    def cek_no_form(self):
        pass
        """
        request = self.request
        session = request.session
        fields  = request.matchdict
        frm = osPbb.frm_split(fields['f'])
        tr = fields['t']
        datas = sipkd_init(self.request, self.context)
        datas['found'] = 0
        datas['spop']=0
        datas['fail']=0

        if  tr in ('21','22'): #'11','12','14',
            data = osMaxBundle.row2dict(osMaxBundle.frm_max(frm));
            if data:
                datas['frm_max']=data['m']
            else:
                datas['frm_max']=data['000']
            
            #cek pada spop
            if frm:
                data=osDOP.row2dict(osDOP.get_by_form(frm))
                if data:
                    datas.update(data)
                    datas['found'] = 1
                    datas['spop']=0
                    datas['fail']=1
                    datas['message']=''.join(('Nomor formulir ', osPbb.frm_join(frm),
                                        ' sudah ada dan tidak boleh dipergunakan lagi !'));
                    return datas
                else: #cek pada lspop        
                    data=osDOPBng.row2dict(osDOPBng.get_by_form(frm))
                    if data:
                        datas['found'] = 1
                        datas.update(data)
                        return datas

        elif  tr in ('23'): #'11','12','14',
            data=osDOPBngDel.row2dict(osDOPBngDel.get_by_form(frm))
            if data['c']>0:
                datas.update(data)
                datas['found'] = 1
                datas['spop']=0
                datas['fail']=1
                datas['message']=''.join(('Nomor formulir ', osPbb.frm_join(frm),
                            ' sudah ada dan tidak boleh dipergunakan lagi !'));
                return datas
        
            elif:
                data = osMaxBundle.row2dict(osMaxBundle.frm_max(frm));
            
            
			  Select max(no_formulir_penghapusan_bng) into vls_dok1 from penghapusan_bng
			  where substr(no_formulir_penghapusan_bng,1,4) = :bl_nop.tx_no_1 and
			    substr(no_formulir_penghapusan_bng,5,4) = :bl_nop.tx_no_2;
			exception when others then vls_dok1 := :bl_nop.tx_no_1||:bl_nop.tx_no_2||'001';
			end;
			if to_number(:bl_nop.tx_no_3) <> (to_number(substr(vls_dok1,9,3))+1) THEN
				Set_Alert_Property('AL_NO_FORM', ALERT_MESSAGE_TEXT, 'Nomor formulir terakhir atas penghapusan bangunan pada bundel ini adalah  '|| 
	  		:bl_nop.tx_no_1||'.'||:bl_nop.tx_no_2||'.'||substr(vls_dok1,9,3)||', diteruskan ... ?');
				vli_alert := Show_Alert('AL_NO_FORM');
				if vli_alert = ALERT_BUTTON2 THEN 
					return 'b';						
				else return 'a';
				end if;
			end if;
    end if;
  
  elsif :bl_nop.tx_jns_trs = '22' THEN
	  if vli_temp > 0 THEN 
	  	if vls_type_no = 'L' THEN
		  	Set_Alert_Property('AL_NO_FORM', ALERT_MESSAGE_TEXT, 'Nomor formulir '|| 
		 		:bl_nop.tx_no_1||'.'||:bl_nop.tx_no_2||'.'||:bl_nop.tx_no_3||' sudah ada dan hanya bisa digunakan untuk NOP '||
		 		vls_prop||'.'||vls_dat||'.'||vls_kec||'.'||vls_kel||'.'||vls_blok||'-'||vls_urut||'.'||vls_jns||', gunakan NOP ini ... ?');
				vli_alert := Show_Alert('al_no_form');
				if vli_alert = ALERT_BUTTON1 THEN
				  :bl_nop.tx_prop := vls_prop;
				  :bl_nop.tx_dat := vls_dat;
				  :bl_nop.tx_kec := vls_kec;
				  :bl_nop.tx_kel := vls_kel;
				  :bl_nop.tx_blk := vls_blok;
				  :bl_nop.tx_urut := vls_urut;
				  :bl_nop.tx_jns := vls_jns;
				  return 'c';
				else return 'a';
				end if;
			else Set_Alert_Property('AL_UMUM', ALERT_MESSAGE_TEXT, 'Nomor formulir '|| 
		 		:bl_nop.tx_no_1||'.'||:bl_nop.tx_no_2||'.'||:bl_nop.tx_no_3||' sudah ada dan hanya bisa digunakan untuk NOP '||
		 		vls_prop||'.'||vls_dat||'.'||vls_kec||'.'||vls_kel||'.'||vls_blok||'-'||vls_urut||'.'||vls_jns||' dengan jenis transaksi 12 !');
				vli_alert := Show_Alert('al_umum');
				return 'a';
			end if;
		elsif to_number(:bl_nop.tx_no_3) <> (to_number(nvl(vls_dok,0))+1) THEN
			Set_Alert_Property('AL_NO_FORM', ALERT_MESSAGE_TEXT, 'Nomor formulir terakhir atas bundel ini adalah  '|| 
  		:bl_nop.tx_no_1||'.'||:bl_nop.tx_no_2||'.'||nvl(vls_dok,'000')||', diteruskan ... ?');
			vli_alert := Show_Alert('AL_NO_FORM');
			if vli_alert = ALERT_BUTTON2 THEN 
				return 'a';
			else return 'b';
			end if;
	  end if;		
  
  end if;
  """

    def get_row(self):
        request = self.request
        session = request.session
        fields  = request.matchdict
        frm = osPbb.frm_split(fields['f'])
        nop = osPbb.nop_split(fields['n1'])
        print 'NOP:',fields['n1']
        datas = sipkd_init(self.request, self.context)
        datas.update(frm)
        datas.update(nop)
        datas['frm_found'] = 0
        datas['spop']=0
        datas['kd_kanwil']=session['kd_kanwil']
        datas['kd_kantor']=session['kd_kantor']
        
        
        #cek pada temp_bundle_sppt
        if frm:
            data=osMaxBundle.get_by_kode(datas)
            if data:
                datas.update(osMaxBundle(row2dict(data)))
                #cek pada spop
                data=osDOP.row2dict(osDOP.get_by_form(frm))
                if data:
                    datas['frm_found'] = 1
                    datas['spop']=1
                    return datas
                    
                #cek pada lspop
                data=osDOPBng.row2dict(osDOPBng.get_by_form(frm))
                if data:
                    datas['frm_found'] = 1
                    datas.update(data)
                    return datas

        data=osDOP.row2dict(osDOP.get_by_kode(datas))
        if data:
            datas['spop_fail'] = 0
        else:
            datas['spop_fail'] = 1
            return datas
            
        row=osMaxBundle.get_max(datas)

        if row[0]:
            datas['frm_max']=row[0]
        else:    
            datas['frm_max']='000'

        if abs(float(datas['frm_max'])-float(datas['temp_urut_bundel']))>1:
            datas['frm_fail']=1
        else:
            datas['frm_fail']=0
        return datas
        
# frm action
    @view_config(route_name='pbblspop',
                 renderer='../../../templates/pbb/lspop.pt')
    def pbblspop(self):
        session = self.request.session
        request = self.request
        resource = None
        url=request.resource_url(resource)
        datas = sipkd_init(request, self.context)
        if session['logged']==0:
            return HTTPFound(location='/')

        
        datas.update(osLSpop.BlankRow())
        schema = osLSpopValid()
        myform = Form(schema, buttons=('btn_save',))
        if 'btn_save' in self.request.POST:
            controls = self.request.POST.items()
            data2=dict((x, y) for x, y in controls)
            datas.update(data2)
            datas['form_visible']= '1'
            datas['readonly'] = 'readonly'
            try:
                appstruct = myform.validate(controls)
                osDOPBng.edit(datas)
            except ValidationFailure, e:
                return dict(datas=datas,
                            url=url)
            data2=cls.BlankRow()
            datas.update(data2)
            datas['form_visible']= '0'
            datas['readonly'] = ''

        return dict(datas=datas,
                    url=url)
#frm keypress                    
    @view_config(route_name='pbblspopc1',
                 renderer='json')
    def pbblspopc1(self):
        datas=self.get_row()
        return json.dumps(datas, default=osPbb.default)
