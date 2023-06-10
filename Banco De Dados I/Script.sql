CREATE DATABASE Metas;

\ c metas
SET
   datestyle TO 'ISO,DMY';

CREATE TABLE IF NOT EXISTS nivelFilial(
   nivelFilial varchar(3) NOT NULL,
   descricao varchar(256) NOT NULL,
   CONSTRAINT pk_nivel (nivelFilial)
) 
CREATE TABLE IF NOT EXISTS metaFilial(
   nivelFilial char(3) NOT NULL,
   vigencia char(6) NOT NULL,
   bonVendedor float NOT NULL,
   bonGerente float NOT NULL,
   CONSTRAINT pk_metaFilial (nivelFilial, vigencia)
) 
CREATE TABLE IF NOT EXISTS nivelVendedor(
   nivelVendedor char(3) NOT NULL,
   descricao char(256) NOT NULL,
   CONSTRAINT pk_nivelVendedor (nivelVendedor)
) 
CREATE TABLE IF NOT EXISTS metaVendedor(
   nivelVendedor char(3) NOT NULL,
   vigencia char(6) NOT NULL,
   pctgMeta float NOT NULL,
   bonificacao float NOT NULL,
   CONSTRAINT pk_metaVendedor (nivelVendedor, vigencia),
   CONSTRAINT fk_nivelVendedor FOREIGN KEY nivelVendedor(nivelVendedor)
) 
CREATE TABLE IF NOT EXISTS localidade(
   codLocal INTEGER AUTO_INCREMENT,
   cidade varchar(20) NOT NULL,
   estado varchar(2) NOT NULL,
   CONSTRAINT pk_localidade (codLocal),
   CONSTRAINT uk_cidadeEstado UNIQUE (cidade, estado)
) 
CREATE TABLE IF NOT EXISTS filial(
   codFilial INTEGER AUTO_INCREMENT,
   -- AUTO INCREMENT faz o código ser incrementado automaticamente
   dtInclusao date NOT NULL,
   dtEncerramento date NULL,
   CNPJ varchar(14) NOT NULL,
   status_filial INTEGER NOT NULL,
   nivelFilial char(3) NOT NULL,
   codLocal INTEGER NOT NULL,
   CONSTRAINT pk_filial (codFilial),
   -- Primary Key com o código da filial
   CONSTRAINT uk_cnpj UNIQUE (cnpj, dtEncerramento),
   -- Chave unica de CNPJ, Data de Encerramento (Permite incluir o mesmo CNPJ diversas vezes, desde que a data de encerramento seja diferente)
   CONSTRAINT fk_local FOREIGN KEY (codLocal) REFERENCES localidade(codLocal),
   -- Chave estrangeira para a localidade
   CONSTRAINT fk_nivel FOREIGN KEY (nivelFilial) REFERENCES nivelFilial(nivelFilial) -- chave estrangeira para o nivel de filial
) 
CREATE TABLE IF NOT EXISTS usuario(
   codUsuario INTEGER AUTO_INCREMENT,
   nome char(256) NOT NULL,
   cpf char(11) NOT NULL UNIQUE,
   login char(256) NOT NULL,
   senha char(256) NOT NULL,
   status_usuario INTEGER NOT NULL,
   dtInclusao date NOT NULL,
   dtEncerramento date NULL,
   tipo INTEGER NOT NULL,
   filial INTEGER NOT NULL,
   nivelVendedor char(3) NULL,
   CONSTRAINT pk_usuario (codUsuario),
   CONSTRAINT uk_cpf UNIQUE (cpf),
   CONSTRAINT fk_filial FOREIGN KEY (filial) REFERENCES filial(codFilial),
   CONSTRAINT fk_nivelVendedor FOREIGN KEY (nivelVendedor) REFERENCES nivelVendedor(nivelVendedor)
) 
CREATE TABLE IF NOT EXISTS venda(
   codVendedor INTEGER NOT NULL UNIQUE,
   -- só um vendedor pode fazer a venda né
   dataVenda date NOT NULL,
   valorFaturado float NOT NULL,
   filial INTEGER NOT NULL UNIQUE,
   CONSTRAINT pk_venda (codVendedor, dataVenda),
   -- e se o vendedor fizer mais que uma venda no mesmo dia?
   CONSTRAINT fk_filial FOREIGN KEY (filial) REFERENCES filial(codFilial)
);

-- Jean vc tem que se decidir, se usa integer ou char para o status de usuario e filial.
-- login em usuario é um datatype eu acho.