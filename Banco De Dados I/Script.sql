create database Metas;
\c locadora
set datestyle to 'ISO,DMY';

create table if not exists nivelFilial(
   nivelFilial varchar(3) NOT NULL,
   Descricao varchar(255) NOT NULL,
   constraint pk_nivel (nivelFilial)
)

create table if not exists localidade(
   codLocal INTEGER AUTO_INCREMENT,
   cidade varchar(20) NOT NULL,
   estado varchar(2) NOT NULL,
   constraint pk_localidade (codLocal)
   constraint uk_cidadeEstado unique (cidade, estado),
)

create table if not exists filial(
   codFilial INTEGER AUTO_INCREMENT, -- AUTO INCREMENT faz o código ser incrementado automaticamente
   dtInclusao date NOT NULL
   dtEncerramento date NULL
   CNPJ varchar(14) NOT NULL,
   ativo varchar(1) NOT NULL,
   nivelFilial char(3) NOT NULL,
   codLocal INTEGER NOT NULL,
   constraint filial_pk_id (codFilial), -- Primary Key com o código da filial
   constraint uk_cnpj unique (cnpj, dtEncerramento), -- Chave unica de CNPJ, Data de Encerramento (Permite incluir o mesmo CNPJ diversas vezes, desde que a data de encerramento seja diferente)
   constraint fk_local foreign key (codLocal) references localidade(codLocal), -- Chave estrangeira para a localidade
   constraint fk_nivel foreign key (nivelFilial) references nivelFilial(nivelFilial) -- chave estrangeira para o nivel de filial
);