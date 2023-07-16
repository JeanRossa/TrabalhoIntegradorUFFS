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
        coduser = $('input:checkbox[name=checkbox_users]:checked').attr('id')
        if (coduser != null) {
            // Aqui é realizado uma requisição GET para o back-end para recuperar todas as informações do usuário
            // É passado o link "/request/usuario" que cai no código /prog1/apps/requests/views.py, que retorna um JSon com as informações para a tela
            axios
                .get('/request/usuario', { params: { cod: coduser } })
                .then(response => {
                    // Popular os fields com os dados retornados
                    $('#id_nome').val(response.data.nome.trim())
                    $('#id_cpf').val(response.data.cpf)
                    $('#id_login').val(response.data.login.trim())
                    $('#id_senha').val(response.data.senha)
                    $('#id_dtinclusao').val(response.data.dtInclusao)
                    $('#id_dtencerramento').val(response.data.dtencerramento)
                    $('#id_status').val(response.data.status).change()
                    $('#id_tipo').val(response.data.tipo).change()
                    $('#id_filial').val(response.data.filial).change()
                    $('#id_nivelvendedor')
                        .val(response.data.nivelvendedor)
                        .change()

                    if (
                        this.id == 'btn_visualizar' ||
                        this.id == 'btn_apagar'
                    ) {
                        if (this.id == 'btn_visualizar') {
                            // Atualizando os valores para visualização
                            document.cookie = 'operation=2' // Visualizar
                            $('#ModalInclusaoLabel').text('Visualizar Usuário') // Título da tela
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
                            $('#ModalInclusaoLabel').text('Excluir Usuário') // Título da tela
                            $('#id_btnok').text('Excluir') // Título do botão
                            $('#id_btnok').removeAttr('hidden') // Aparecer botão
                        }

                        // Bloquear campos impedindo a edição
                        $('#id_nome').attr('readonly', 'readonly')
                        $('#id_tipo').attr(
                            'onchange',
                            "this.value = '" + response.data.tipo + "'"
                        )
                        $('#id_filial').attr(
                            'onchange',
                            "this.value = '" + response.data.filial + "'"
                        )
                        $('#id_nivelvendedor').attr(
                            'onchange',
                            "this.value = '" + response.data.nivelvendedor + "'"
                        )
                        $('#id_status').attr(
                            'onchange',
                            "this.value = '" + response.data.status + "'"
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
                        // Atualizar labels da tela
                        $('#ModalInclusaoLabel').text('Editar Usuário')
                        $('#id_btnok').text('Salvar')
                        // Desbloquear campos editavies
                        $('#id_btnok').removeAttr('hidden')
                        $('#id_nome').removeAttr('readonly')
                        $('#id_tipo').removeAttr('onchange')
                        $('#id_filial').removeAttr('onchange')
                        $('#id_nivelvendedor').removeAttr('onchange')
                        $('#id_status').removeAttr('onchange')
                    }
                    // Bloquear campos não editaveis/demais campos para visualização
                    $('#id_cpf').attr('readonly', 'readonly')
                    $('#id_login').attr('readonly', 'readonly')
                    $('#id_senha').attr('readonly', 'readonly')
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
    $('#id_btnok').removeAttr('hidden')
    $('#id_nome').removeAttr('readonly')
    $('#id_cpf').removeAttr('readonly')
    $('#id_login').removeAttr('readonly')
    $('#id_senha').removeAttr('readonly')
    $('#id_tipo').removeAttr('onchange')
    $('#id_tipo').removeAttr('onchange')
    $('#id_filial').removeAttr('onchange')
    $('#id_nivelvendedor').removeAttr('onchange')
    $('#id_status').removeAttr('readonly')
    // Impedir alterção do status
    $('#id_status').attr('onchange', "this.value = '1'")
    // Resetar campos para o padrão
    $('#id_status').val('1').change()
    $('#id_tipo').val('').change()
    $('#id_filial').val('').change()
    $('#id_nivelvendedor').val('').change()
    // Limpar campos
    $('#id_nome').val('')
    $('#id_cpf').val('')
    $('#id_login').val('')
    $('#id_senha').val('')
    $('#id_dtinclusao').val('')
    $('#id_dtencerramento').val('')
    // Abrir tela
    $('#ModalInclusao').modal('toggle')
})
