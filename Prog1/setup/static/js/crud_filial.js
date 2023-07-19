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
        codfilial = $('input:checkbox[name=checkbox_branches]:checked').attr(
            'id'
        )
        if (codfilial != null) {
            // Aqui é realizado uma requisição GET para o back-end para recuperar todas as informações do usuário
            // É passado o link "/request/filial" que cai no código /prog1/apps/requests/views.py, que retorna um JSon com as informações para a tela
            axios
                .get('/request/filial', { params: { cod: codfilial } })
                .then(response => {
                    // Popular os fields com os dados retornados

                    $('#id_cnpj').val(response.data.cnpj)
                    $('#id_dtinclusao').val(response.data.dtInclusao)
                    $('#id_dtencerramento').val(response.data.dtencerramento)
                    $('#id_status').val(response.data.status).change()
                    $('#id_nivelfilial').val(response.data.nivelfilial).change()
                    $('#id_codlocal').val(response.data.codlocal).change()

                    if (
                        this.id == 'btn_visualizar' ||
                        this.id == 'btn_apagar'
                    ) {
                        if (this.id == 'btn_visualizar') {
                            // Atualizando os valores para visualização
                            document.cookie = 'operation=2' // Visualizar
                            $('#ModalInclusaoLabel').text('Visualizar Filial') // Título da tela
                            $('#id_btnok').attr('hidden', 'hidden') // Esconder botão
                        } else {
                            // Valida se é possível editar
                            if (response.data.status == '2') {
                                alert(
                                    'Não é permitida exclusão de registros já excluidos/inativos'
                                )
                                return
                            }
                            // Atualizando valores para exclusão
                            document.cookie = 'operation=4' // Exclusão
                            document.cookie = 'codfilial=' + codfilial // Código da filial
                            $('#ModalInclusaoLabel').text('Excluir Filial') // Título da tela
                            $('#id_btnok').text('Excluir') // Título do botão
                            $('#id_btnok').removeAttr('hidden') // Aparecer botão
                        }

                        // Bloquear campos impedindo a edição
                        $('#id_cnpj').attr('readonly', 'readonly')
                        $('#id_status').attr(
                            'onchange',
                            "this.value = '" + response.data.status + "'"
                        )
                        $('#id_nivelfilial').attr(
                            'onchange',
                            "this.value = '" + response.data.nivelfilial + "'"
                        )
                        $('#id_codlocal').attr(
                            'onchange',
                            "this.value = '" + response.data.codlocal + "'"
                        )
                    } else if (this.id == 'btn_editar') {
                        // Validar se é possível editar
                        if (response.data.status == '2') {
                            alert(
                                'Não é permitida edição de registros já excluidos/inativos'
                            )
                            return
                        }
                        // Atualizar operação que o usuário está realizando
                        document.cookie = 'operation=3'
                        document.cookie = 'codfilial=' + codfilial
                        // Atualizar labels da tela
                        $('#ModalInclusaoLabel').text('Editar Filial')
                        $('#id_btnok').text('Salvar')
                        // Desbloquear campos editavies
                        $('#id_btnok').removeAttr('hidden')
                        $('#id_cnpj').removeAttr('readonly')
                        $('#id_status').removeAttr('onchange')
                        $('#id_nivelfilial').removeAttr('onchange')
                        $('#id_codlocal').removeAttr('onchange')
                    }
                    // Bloquear campos não editaveis/demais campos para visualização
                    $('#id_cnpj').attr('readonly', 'readonly')
                    // Abrir tela modal
                    $('#ModalInclusao').modal('toggle')
                })
        } else {
            alert('Selecione um registro')
        }
    })

// Função chamada na inclusão
$('#btn_incluir').click(function () {
    // Atualizar operação que o usuário está realizando
    document.cookie = 'operation=1'
    // Atualizar labels da tela
    $('#ModalInclusaoLabel').text('Incluir Filial')
    $('#id_btnok').text('Salvar')

    // Desbloquear campos para permitir edição
    $('#id_cnpj').removeAttr('disabled')
    $('#id_nivelfilial').removeAttr('disabled')
    $('#id_status').removeAttr('disabled')
    $('#id_dtinclusao').removeAttr('disabled')
    $('#id_dtencerramento').removeAttr('disabled')

    // Impedir alteração do status
    $('#id_status').attr('onchange', "this.value = '1'")
    $('#id_dtinclusao').attr('onchange')
    $('#id_dtencerramento').attr('onchange')

    // Resetar campos para o padrão
    $('#id_status').val('1').change()
    $('#id_cnpj').val('').change()
    $('#id_nivelfilial').val('').change()
    $('#id_codlocal').val('').change()

    // Limpar campos
    $('#id_cnpj').val('')
    $('#id_dtinclusao').val('')
    $('#id_dtencerramento').val('')

    $('#ModalInclusao').modal('toggle')
})
