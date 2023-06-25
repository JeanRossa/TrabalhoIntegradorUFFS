// the selector will match all input controls of type :checkbox
// and attach a click event handler 
$('input[type="checkbox"]').on('change', function() {
	$('input[type="checkbox"]').not(this).prop('checked', false);
 });

 $('#btn_visualizar').click(function() {

	$('#id_modalInclusaoLabel').text('Visualizar Usuário');
	$('#id_btnok'		      ).text('Sair');

	$('#id_nome'		  ).attr('disabled','disabled');
	$('#id_cpf'			  ).attr('disabled','disabled');
	$('#id_login'		  ).attr('disabled','disabled');
	$('#id_senha'		  ).attr('disabled','disabled');
	$('#id_dtinclusao'	  ).attr('disabled','disabled');
	$('#id_dtencerramento').attr('disabled','disabled');
	$('#id_tipo'		  ).attr('disabled','disabled');
	$('#id_filial'		  ).attr('disabled','disabled');
	$('#id_nivelvendedor' ).attr('disabled','disabled');
	$('#id_status' 		  ).attr('disabled','disabled');
	
	$('#id_nome'		  ).val('1');
	$('#id_cpf'			  ).val('1');
	$('#id_login'		  ).val('2');
	$('#id_senha'		  ).val('3');
	$('#id_dtinclusao'	  ).val('1');
	$('#id_dtencerramento').val('2');
	
	$('#id_status'		  ).val("2").change();
	$('#id_tipo'		  ).val("1").change();
	$('#id_filial'		  ).val("2").change();
	$('#id_nivelvendedor' ).val("2").change();
	
	$('#ModalInclusao'	  ).modal('toggle');
});

$('#btn_incluir').click(function() {
	
	var d = new Date();
	dataHora = (d.toLocaleString());    

	$('#id_modalInclusaoLabel').text('Incluir Usuário');
	$('#id_btnok'		      ).text('Salvar');
	
	$('#id_nome'		  ).removeAttr('disabled');
	$('#id_cpf'			  ).removeAttr('disabled');
	$('#id_login'		  ).removeAttr('disabled');
	$('#id_senha'		  ).removeAttr('disabled');
	$('#id_tipo'		  ).removeAttr('disabled');
	$('#id_filial'		  ).removeAttr('disabled');
	$('#id_nivelvendedor' ).removeAttr('disabled');
	$('#id_status'		  ).removeAttr('disabled');
	$('#id_dtinclusao'	  ).removeAttr('disabled');
	$('#id_dtencerramento').removeAttr('disabled');

	$('#id_status'		  ).val("1").change();
	$('#id_tipo'		  ).val("" ).change();
	$('#id_filial'		  ).val("" ).change();
	$('#id_nivelvendedor' ).val("" ).change();

	$('#id_status'		  ).attr('onchange',"this.value = '1'");

	$('#id_nome'		  ).val('');
	$('#id_cpf'			  ).val('');
	$('#id_login'		  ).val('');
	$('#id_senha'		  ).val('');
	$('#id_dtinclusao'	  ).val('');
	$('#id_dtencerramento').val('');

	$('#ModalInclusao'	  ).modal('toggle');
});

const getRequest = async () => {
	const response = await axios.get('/request/usuario', {
		params: {
			'cod': 18
		}
	})
	console.log(response.data)
}
	getRequest();