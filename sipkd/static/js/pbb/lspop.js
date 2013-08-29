$(document).ready(function () {
  function set_value(data) {
    $("#kd_propinsi").val(data['kd_propinsi']);
    $("#kd_dati2").val(data['kd_dati2']);
    $("#kd_kecamatan").val(data['kd_kecamatan']);
    $("#kd_kelurahan").val(data['kd_kelurahan']);
    $("#kd_blok").val(data['kd_blok']);
    $("#no_urut").val(data['no_urut']);
    $("#kd_jns_op").val(data['kd_jns_op']);
    $("#no_bng").val(data['no_bng']);
    $("#kd_jpb").val(data['kd_jpb']);
    $("#no_formulir_lspop").val(data['no_formulir_lspop']);
    $("#thn_dibangun_bng").val(data['thn_dibangun_bng']);
    $("#thn_renovasi_bng").val(data['thn_renovasi_bng']);
    $("#luas_bng").val(data['luas_bng']);
    $("#jml_lantai_bng").val(data['jml_lantai_bng']);
    $("#kondisi_bng").val(data['kondisi_bng']);
    $("#jns_konstruksi_bng").val(data['jns_konstruksi_bng']);
    $("#jns_atap_bng").val(data['jns_atap_bng']);
    $("#kd_dinding").val(data['kd_dinding']);
    $("#kd_lantai").val(data['kd_lantai']);
    $("#kd_langit_langit").val(data['kd_langit_langit']);
    $("#nilai_sistem_bng").val(data['nilai_sistem_bng']);
    $("#jns_transaksi_bng").val(data['jns_transaksi_bng']);
    $("#tgl_pendataan_bng").val(data['tgl_pendataan_bng']);
    $("#nip_pendata_bng").val(data['nip_pendata_bng']);
    $("#tgl_pemeriksaan_bng").val(data['tgl_pemeriksaan_bng']);
    $("#nip_pemeriksa_bng").val(data['nip_pemeriksa_bng']);
    $("#tgl_perekaman_bng").val(data['tgl_perekaman_bng']);
    $("#nip_perekam_bng").val(data['nip_perekam_bng']);
  }

  function readonly() {
    return false
    if ($("#form_visible").val() == 0) {
      //$("#data").css('display', 'None');
      $("#btn_validate").css('visibility', 'visible');
      $("#btn_save").attr('disabled', 'disabled');

      $("#kd_kecamatan").removeAttr('readonly');
      $("#kd_kelurahan").removeAttr('readonly');
      $("#kd_blok").removeAttr('readonly');
      $("#no_urut").removeAttr('readonly');
      $("#kd_jns_op").removeAttr('readonly');

      $("#frm1").removeAttr('readonly');
      $("#frm2").removeAttr('readonly');
      $("#frm3").removeAttr('readonly');

    } else {

      $("#data").css('display', 'block');
      $("#btn_validate").css('visibility', 'hidden');
      $("#btn_save").removeAttr('disabled');

      $("#kd_kecamatan").attr('readonly', 'readonly');
      $("#kd_kelurahan").attr('readonly', 'readonly');
      $("#kd_blok").attr('readonly', 'readonly');
      $("#no_urut").attr('readonly', 'readonly');
      $("#kd_jns_op").attr('readonly', 'readonly');

      $("#jns_transaksi_op").attr('readonly', 'readonly');

      $("#frm1").attr('readonly', 'readonly');
      $("#frm2").attr('readonly', 'readonly');
      $("#frm3").attr('readonly', 'readonly');

    }
  }
  readonly();

  $("#btn_validate").click(function () {

    var trans = $("#jns_transaksi_op").val();

    var frm1 = $("#frm1").val();
    var frm2 = $("#frm2").val();
    var frm3 = $("#frm3").val();

    var kd_propinsi = $("#kd_propinsi").val();
    var kd_dati2 = $("#kd_dati2").val();

    var kd_kecamatan = $("#kd_kecamatan").val();
    var kd_kelurahan = $("#kd_kelurahan").val();
    var kd_blok = $("#kd_blok").val();
    var no_urut = $("#no_urut").val();
    var kd_jns_op = $("#kd_jns_op").val();

    if (isNaN(frm1) || isNaN(frm2) || isNaN(frm3) || isNaN(kd_kecamatan) || isNaN(kd_kelurahan) 
        || isNaN(kd_blok) || isNaN(no_urut) || isNaN(kd_jns_op) || isNaN(trans) || !frm1 || !frm2 || !frm3 
        || !kd_kecamatan || !kd_kelurahan || !kd_blok || !kd_jns_op || !no_urut || !jns_transaksi_op) {
      alert('Lengkapi Isian Form');
      return false;
    }


    var nop = kd_propinsi + '.' + kd_dati2 + '-' + kd_kecamatan + '.' + kd_kelurahan +
      '.' + kd_blok + '.' + no_urut + '.' + kd_jns_op;

    var fmsg = "";
    //cek Tahun
    var d = new Date();
    var vls_tahun = d.getFullYear();
    if (frm1.length != 4) fmsg = 'Inputan untuk tahun harus 4 digit !';
    if (frm1 < 1900) fmsg = 'Inputan untuk tahun tidak valid !';
    if (frm1.length != 4 && frm1 != vls_thn) {
      cmsg = 'Yakin Isian tahun bukan tahun ' + vlstahun;
      if (confirm(cmsg) == false) return false;
    }

    //cek bundle
    if (frm2.length != 4) fmsg = 'Inputan nomor buku/bundel tidak boleh kosong dan harus 4 digit !';
    if (frm2 < 1) fmsg = 'Inputan nomor buku/bundel tidak valid !';
    //cek no_urut
    if (frm3.length != 3) fmsg = 'Inputan nomor urut formulir tidak boleh kosong dan harus 3 digit !';
    if (frm3 < 1) fmsg = 'Inputan nomor formulir tidak valid !';

    if (no_urut < 1) fmsg = 'Inputan nomor urut tidak boleh 0000!';

    if (kd_blok != '000') {
      kd_jns_op = '0';
      $('#kd_jns_op').val(kd_jns_op);
    }

    
    if ($("#form_visible").val() == '0') {
      $.ajax({
        url: '/pbb/lspop/c/' + trans + '/' + frm1 + frm2 + frm3 + '/' + kd_kecamatan + kd_kelurahan + kd_blok + no_urut + kd_jns_op,
        success: function (json) {
          data = JSON.parse(json);

          if (data['frm_found'] == 1) {
            if (data['spop'] == 1) {
              var nopmsg = 'No. Form sudah digunakan pada SPOP ';
              alert(nopmsg);
              return false;
            }  

            var nopmsg = 'No. Form sudah digunakan untuk NOP: ' +
              data['kd_propinsi'] + '.' + data['kd_dati2'] + '-' + data['kd_kecamatan'] + '.' + data['kd_kelurahan'] + '-' +
              data['kd_blok'] + '.' + data['no_urut'] + '.' + data['kd_jns_op'];
            if (trans == 1) { //tambah
              alert(nopmsg);
              return false;
            } else {
              if (trans == 2) { //edit
                if (confirm(nopmsg + ' gunakan NOP?') == false) {
                  return false;
                } else {
                  set_value(data);
                };
              } else {
                return false
              }
            }
          }
           
          if (data['spop_fail'] == "1") {
            var nopmsg = 'NOP Tidak Ditemukan Dalam Database ';
            alert(nopmsg);
            return false;
          }

          if (data['frm_fail'] == "1") {
            var c = confirm('No Urut Terakhir ' + data['frm_max'] + ' Lanjutkan?');
            if (!c) return false;
          }
          
          $("#form_visible").val('1');
          readonly();

        },
        error: function (xhr, desc, er) {
          alert(er);
        }
      });
    }
  });


  $("#btn_save").click(function () {
    $("#myform").submit();
  })

  $("#btn_reset").click(function () {
    $("#form_visible").val('0');
    readonly();
  });

});