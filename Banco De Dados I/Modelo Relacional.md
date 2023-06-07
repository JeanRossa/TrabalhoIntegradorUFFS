filial(<ins>codFilial</ins>, gerente(usuario), dtInclusao, dtEncerramento, cnpj, status, nivelFilial(nivelFilial), localizacao(localidade))

usuario(<ins>codUsuario</ins>, nome, cpf, login, email, senha, status, dtInclusao, dtEncerramento, tipo, filial(filial))

localidade(<ins>cidade</ins>, <ins>estado</ins>)

nivelFilial(<ins>nivelFilial</ins>, descricao)

nivelVendedor(<ins>nivelVendedor</ins>, descricao)

metaFilial(<ins>nivelFilial(nivelFilial)</ins>, <ins>vigencia</ins>, bonVendedor, bonGerente)

metaVendedor(<ins>vigencia, nivelVend(nivelVendedor)</ins>, pctgMeta, bonificacao)

venda(<ins>vendedor(usuario)</ins>, <ins>data</ins>, valorFaturado, filial(filial))