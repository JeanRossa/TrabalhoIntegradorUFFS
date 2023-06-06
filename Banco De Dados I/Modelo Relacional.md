<span style="border-bottom: 2px dashed;">Text with a dashed line underneath</span>


filial(<ins>codFilial</ins>, gerente(usuario), dtInclusao, dtEncerramento, cnpj, status, nvFilial(nivelFilial), localizacao(localidade))

usuario(<ins>codUsuario</ins>, nome, cpf, login, email, senha, status, dtInclusao, dtEncerramento, tipo, filial(filial))

localidade(<ins>cidade</ins>, <ins>estado</ins>)

nivelFilial(<ins>nivelFilial</ins>, descricao)

nivelVendedor(<ins>nivelVendedor</ins>, descricao)

metaFilial(<ins>nivelFilial(nivelFilial)</ins>, <ins>vigencia</ins>, bonVendedor, bonGerente)

metaVendedor(<ins>vigencia, nivelVend(nivelVendedor)</ins>, pctgMeta, bonificacao)

venda(<ins>vendedor(usuario)</ins>, <ins>data</ins>, valorFaturado, filial(filial))
 
É necessário estabelecer uma relação entre as vendas e as filiais, considerando que os vendedores já estão associados às respectivas filiais? Além disso, a meta de vendas dos vendedores deve estar relacionada à meta das filiais, levando em conta a complexidade do caminho de volta.

Como associar o vendedor com a sua meta ja que gerentes não as possuem, então não é possivel associar as metas no cadastro do usuario.

Eu posso colocar a coluna meta 