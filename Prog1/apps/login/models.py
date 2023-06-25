# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime


class Filial(models.Model):
    codfilial = models.AutoField(primary_key=True)
    dtinclusao = models.DateField()
    dtencerramento = models.DateField(blank=True, null=True)
    cnpj = models.CharField(max_length=14)
    status = models.IntegerField()
    nivelfilial = models.ForeignKey('Nivelfilial', models.DO_NOTHING, db_column='nivelfilial')
    codlocal = models.ForeignKey('Localidade', models.DO_NOTHING, db_column='codlocal')

    class Meta:
        managed = False
        db_table = 'filial'
        unique_together = (('cnpj', 'dtencerramento'),)

    def __str__(self):
        return "Filial " + str(self.codfilial)


class Localidade(models.Model):
    codlocal = models.AutoField(primary_key=True)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'localidade'
        unique_together = (('cidade', 'estado'),)


class Metafilial(models.Model):
    nivelfilial = models.CharField(primary_key=True, max_length=3)  # The composite primary key (nivelfilial, vigencia) found, that is not supported. The first column is selected.
    vigencia = models.CharField(max_length=6)
    bonvendedor = models.FloatField()
    bongerente = models.FloatField()

    class Meta:
        managed = False
        db_table = 'metafilial'
        unique_together = (('nivelfilial', 'vigencia'),)


class Metavendedor(models.Model):
    nivelvendedor = models.OneToOneField('Nivelvendedor', models.DO_NOTHING, db_column='nivelvendedor', primary_key=True)  # The composite primary key (nivelvendedor, vigencia) found, that is not supported. The first column is selected.
    vigencia = models.CharField(max_length=6)
    pctgmeta = models.FloatField()
    bonificacao = models.FloatField()

    class Meta:
        managed = False
        db_table = 'metavendedor'
        unique_together = (('nivelvendedor', 'vigencia'),)


class Nivelfilial(models.Model):
    nivelfilial = models.CharField(primary_key=True, max_length=3)
    descricao = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'nivelfilial'


class Nivelvendedor(models.Model):
    nivelvendedor = models.CharField(primary_key=True, max_length=3)
    descricao = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'nivelvendedor'

    def __str__(self):
        return "Nivel " + self.nivelvendedor + " - " + self.descricao


class Usuario(models.Model):

    OPC_STATUS = [
        (1, "Ativo"),
        (2, "Inativo"),
    ]

    OPC_TIPO = [
        (1, "Administrador"),
        (2, "Gerente"),
        (3, "Vendedor"),
    ]

    codusuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=256)
    cpf = models.CharField(max_length=11)
    login = models.CharField(max_length=256)
    senha = models.CharField(max_length=256)
    status = models.IntegerField(default=1, choices=OPC_STATUS)
    dtinclusao = models.DateField(default=datetime.now, blank=True)
    dtencerramento = models.DateField(blank=True, null=True)
    tipo = models.IntegerField(choices=OPC_TIPO)
    filial = models.ForeignKey(Filial, models.DO_NOTHING, db_column='filial', blank=True, null=True)
    nivelvendedor = models.ForeignKey(Nivelvendedor, models.DO_NOTHING, db_column='nivelvendedor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

class Venda(models.Model):
    codvendedor = models.IntegerField(primary_key=True)  # The composite primary key (codvendedor, datavenda) found, that is not supported. The first column is selected.
    datavenda = models.DateField()
    valorfaturado = models.FloatField()
    filial = models.OneToOneField(Filial, models.DO_NOTHING, db_column='filial')

    class Meta:
        managed = False
        db_table = 'venda'
        unique_together = (('codvendedor', 'datavenda'),)
