<span style="border-bottom: 2px dashed;">Text with a dashed line underneath</span>


filial(<ins>cod</ins>, gerente(usuario), dtInclusao, dtEncerramento, cnpj, status, nvFilial(nivelFilial), localizacao(localidade))

tipoUsuario(<ins>cod</ins>, descricao)

usuario(<ins>cod</ins>, nome, cpf, login*, email*, senha, status, dtInclusao, dtEncerramento, tipo(tipoUsuario), filial(filial))

localidade(<ins>cidade</ins>, <ins>estado</ins>)

nivelFilial(<ins>nivel</ins>, <ins>descricao</ins>)

nivelVendedor(<ins>nivel</ins>, descricao, metaVendedor(metaVendededor))

metaFilial(<ins>nvFilial(nivelFilial)</ins>, <ins>vigencia</ins>, bonVendedor, bonGerente)

metaVendedor(<ins>vigencia</ins>, pctgMeta, bonificacao)

venda(<ins>vendedor(usuario)</ins>, <ins>data</ins>, valorFaturado, filial(filial))
 
É necessário estabelecer uma relação entre as vendas e as filiais, considerando que os vendedores já estão associados às respectivas filiais? Além disso, a meta de vendas dos vendedores deve estar relacionada à meta das filiais, levando em conta a complexidade do caminho de volta.

Como associar o vendedor com a sua meta ja que gerentes não as possuem, então não é possivel associar as metas no cadastro do usuario.

Eu posso colocar a coluna meta 