// Função ativada toda vez que é selecionado um CheckBox, permite somente um selecionado em toda a tela
$('input[type="checkbox"]').on('change', function () {
    $('input[type="checkbox"]').not(this).prop('checked', false)
})

// Função chamada para os botões de Visualizar, editar e excluir
$('#btn_visualizar').add('#btn_editar').add('#btn_apagar').on('click', function () {
        // Pegar código selecionado
        nivelfilial = $('input:checkbox[name=checkbox_branchLevels]:checked').attr('id')
        if (nivelfilial != null) {
            // Aqui é realizado uma requisição GET para o back-end para recuperar todas as informações do Nível de Filial
            // É passado o link "/request/nivelFilial" que cai no código /prog1/apps/requests/views.py, que retorna um JSon com as informações para a tela
            axios
                .get('/request/nivelfilial', { params: { cod: nivelfilial } }).then(response => {
                    // Popular os fields com os dados retornados
                    $('#id_nivelfilial').val(response.data.nivelfilial)
                    $('#id_descricao').val(response.data.descricao.trim())

                    if (this.id == 'btn_visualizar' || this.id == 'btn_apagar') {
                        if (this.id == 'btn_visualizar') {
                            // Atualizando os valores para visualização
                            document.cookie = 'operation=2' // Visualizar
                            $('#ModalInclusaoLabel').text('Visualizar Nível de Filial') // Título da tela
                            $('#id_btnok').attr('hidden', 'hidden') // Esconder botão
                        } else {
                            // Atualizando valores para exclusão
                            document.cookie = 'operation=4' // Exclusão
                            $('#ModalInclusaoLabel').text('Excluir Nível de Filial') // Título da tela
                            $('#id_btnok').text('Excluir') // Título do botão
                            $('#id_btnok').removeAttr('hidden') // Aparecer botão
                        }

                        // Bloquear campos impedindo a edição
                        $('#id_nivelfilial').attr('readonly', 'readonly')
                        $('#id_descricao').attr('readonly', 'readonly')
                    } else if (this.id == 'btn_editar') {
                        // Atualizar operação que o Nível de Filial está realizando
                        document.cookie = 'operation=3'
                        document.cookie = 'codigo=' + nivelfilial
                        // Atualizar labels da tela
                        $('#ModalInclusaoLabel').text('Editar Nível de Filial')
                        $('#id_btnok').text('Salvar')
                        // Desbloquear campos editavies
                        $('#id_btnok').removeAttr('hidden')
                        $('#id_descricao').removeAttr('readonly')
                        $('#id_nivelfilial').attr('readonly', 'readonly')
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
    $('#ModalInclusaoLabel').text('Incluir Nível de Filial')
    $('#id_btnok').text('Salvar')
    document.cookie = 'operation=1'

    $('#id_btnok').removeAttr('hidden')
    $('#id_nivelfilial').removeAttr('readonly')
    $('#id_descricao').removeAttr('readonly')

    $('#id_nivelfilial').val('').change()
    $('#id_descricao').val('').change()

    $('#ModalInclusao').modal('toggle')
})
