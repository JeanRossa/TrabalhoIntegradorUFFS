// Função ativada toda vez que é selecionado um CheckBox, permite somente um selecionado em toda a tela
$('input[type="checkbox"]').on('change', function () {
  $('input[type="checkbox"]').not(this).prop('checked', false)
})

// Função chamada para os botões de Visualizar, editar e excluir
$('#btn_visualizar')
  .add('#btn_editar')
  .add('#btn_apagar')
  .on('click', function () {
    // Pegar código selecionado
    codlocal = $('input:checkbox[name=checkbox_sites]:checked').attr('id')
    if (codlocal != null) {
      // Aqui é realizado uma requisição GET para o back-end para recuperar todas as informações do Localidade
      // É passado o link "/request/localidade" que cai no código /prog1/apps/requests/views.py, que retorna um JSon com as informações para a tela
      axios
        .get('/request/localidade', { params: { cod: codlocal } })
        .then(response => {
          // Popular os fields com os dados retornados
          $('#id_cidade').val(response.data.cidade.trim())
          $('#id_estado').val(response.data.estado)

          if (this.id == 'btn_visualizar' || this.id == 'btn_apagar') {
            if (this.id == 'btn_visualizar') {
              // Atualizando os valores para visualização
              document.cookie = 'operation=2' // Visualizar
              $('#ModalInclusaoLabel').text('Visualizar Localidade') // Título da tela
              $('#id_btnok').attr('hidden', 'hidden') // Esconder botão
            } else {
              // Atualizando valores para exclusão
              document.cookie = 'operation=4' // Exclusão
              $('#ModalInclusaoLabel').text('Excluir Localidade') // Título da tela
              $('#id_btnok').text('Excluir') // Título do botão
              $('#id_btnok').removeAttr('hidden') // Aparecer botão
            }

            // Bloquear campos impedindo a edição
            $('#id_cidade').attr('readonly', 'readonly')
            $('#id_estado').attr(
              'onchange',
              "this.value = '" + response.data.estado + "'"
            )
          } else if (this.id == 'btn_editar') {
            // Atualizar operação que o Localidade está realizando
            document.cookie = 'operation=3'
            // Atualizar labels da tela
            $('#ModalInclusaoLabel').text('Editar Localidade')
            $('#id_btnok').text('Salvar')
            // Desbloquear campos editavies
            $('#id_btnok').removeAttr('hidden')
            $('#id_cidade').removeAttr('readonly')
            $('#id_estado').removeAttr('onchange')
          }
          // Bloquear campos não editaveis/demais campos para visualização
          // Abrir tela modal
          $('#ModalInclusao').modal('toggle')
        })
    } else {
      alert('Selecione um registro')
    }
  })

// Função chamada na inclusão
$('#btn_incluir').click(function () {
  $('#id_modalInclusaoLabel').text('Incluir Localidade')
  $('#id_btnok').text('Salvar')

  $('#id_cidade').removeAttr('readonly')
  $('#id_estado').removeAttr('onchange')

  $('#id_cidade').val('').change()
  $('#id_estado').val('').change()

  $('#id_status').attr('onchange', "this.value = '1'")
  $('#ModalInclusao').modal('toggle')
})
