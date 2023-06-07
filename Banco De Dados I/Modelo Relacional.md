<head>
    <link rel="stylesheet" href="styles.css">
</head>

filial(<ins>codFilial</ins>, gerente(usuario), dtInclusao, dtEncerramento, cnpj, status, nivelFilial(nivelFilial),
localizacao(localidade))

usuario(<ins>codUsuario</ins>, nome, cpf, login, email, senha, status, dtInclusao, dtEncerramento, tipo, <span class="dashed-line">filial</span>(filial), <span class="dashed-line">nivelVendedor</span>(nivelVendedor))

localidade(<ins>cidade</ins>, <ins>estado</ins>)

nivelFilial(<ins>nivelFilial</ins>, descricao)

nivelVendedor(<ins>nivelVendedor</ins>, descricao)

metaFilial(<ins>nivelFilial</ins>(nivelFilial), <ins>vigencia</ins>, bonVendedor, bonGerente)

metaVendedor(<ins>nivelVend</ins>(nivelVendedor),<ins>Vigência</ins>, pctgMeta, bonificacao)

venda(<ins>vendedor</ins>(usuario), <ins>data</ins>, valorFaturado, filial(filial))