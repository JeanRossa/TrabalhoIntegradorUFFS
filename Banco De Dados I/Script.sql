CREATE DATABASE Metas;

\ c metas
SET
   datestyle TO 'ISO,DMY';

CREATE TABLE IF NOT EXISTS nivelFilial(
   nivelFilial char(3) NOT NULL,
   descricao char(256) NOT NULL,
   CONSTRAINT pk_nivelFilial PRIMARY KEY (nivelFilial)
);

CREATE TABLE IF NOT EXISTS metaFilial(
   nivelFilial char(3) NOT NULL,
   vigencia char(6) NOT NULL,
   bonVendedor float NOT NULL,
   bonGerente float NOT NULL,
   CONSTRAINT pk_metaFilial PRIMARY KEY (nivelFilial, vigencia)
);

CREATE TABLE IF NOT EXISTS nivelVendedor(
   nivelVendedor char(3) NOT NULL,
   descricao char(256) NOT NULL,
   CONSTRAINT pk_nivelVendedor PRIMARY KEY (nivelVendedor)
);

CREATE TABLE IF NOT EXISTS metaVendedor(
   nivelVendedor char(3) NOT NULL,
   vigencia char(6) NOT NULL,
   pctgMeta float NOT NULL,
   bonificacao float NOT NULL,
   CONSTRAINT pk_metaVendedor PRIMARY KEY (nivelVendedor, vigencia),
   CONSTRAINT fk_nivelVendedor FOREIGN KEY (nivelVendedor) REFERENCES nivelVendedor(nivelVendedor)
);

CREATE TABLE IF NOT EXISTS localidade(
   codLocal SERIAL,
   cidade varchar(20) NOT NULL,
   estado varchar(2) NOT NULL,
   CONSTRAINT pk_localidade PRIMARY KEY (codLocal),
   CONSTRAINT uk_cidadeEstado UNIQUE (cidade, estado)
);

CREATE TABLE IF NOT EXISTS filial(
   codFilial SERIAL,
   -- SERIAL faz o código ser incrementado automaticamente
   dtInclusao date NOT NULL,
   dtEncerramento date NULL,
   CNPJ varchar(14) NOT NULL,
   "status" INTEGER NOT NULL,
   nivelFilial char(3) NOT NULL,
   codLocal INTEGER NOT NULL,
   CONSTRAINT pk_filial PRIMARY KEY (codFilial),
   -- Primary Key com o código da filial
   CONSTRAINT uk_cnpj UNIQUE (cnpj, dtEncerramento),
   -- Chave unica de CNPJ, Data de Encerramento (Permite incluir o mesmo CNPJ diversas vezes, desde que a data de encerramento seja diferente)
   CONSTRAINT fk_local FOREIGN KEY (codLocal) REFERENCES localidade(codLocal),
   -- Chave estrangeira para a localidade
   CONSTRAINT fk_nivel FOREIGN KEY (nivelFilial) REFERENCES nivelFilial(nivelFilial) -- chave estrangeira para o nivel de filial
);

CREATE TABLE IF NOT EXISTS usuario(
   codUsuario SERIAL,
   nome char(256) NOT NULL,
   cpf char(11) NOT NULL UNIQUE,
   login char(256) NOT NULL,
   senha char(256) NOT NULL,
   "status" INTEGER NOT NULL,
   dtInclusao date NOT NULL,
   dtEncerramento date NULL,
   tipo INTEGER NOT NULL,
   filial INTEGER NULL,
   nivelVendedor char(3) NULL,
   CONSTRAINT pk_usuario PRIMARY KEY (codUsuario),
   CONSTRAINT uk_cpf UNIQUE (cpf, dtEncerramento),
   CONSTRAINT fk_filial FOREIGN KEY (filial) REFERENCES filial(codFilial),
   CONSTRAINT fk_nivelVendedor FOREIGN KEY (nivelVendedor) REFERENCES nivelVendedor(nivelVendedor)
);

CREATE TABLE IF NOT EXISTS venda(
   codVendedor INTEGER NOT NULL UNIQUE,
   -- só um vendedor pode fazer a venda né
   dataVenda date NOT NULL,
   valorFaturado float NOT NULL,
   filial INTEGER NOT NULL UNIQUE,
   CONSTRAINT pk_venda PRIMARY KEY (codVendedor, dataVenda),
   -- e se o vendedor fizer mais que uma venda no mesmo dia?
   CONSTRAINT fk_filial FOREIGN KEY (filial) REFERENCES filial(codFilial)
);