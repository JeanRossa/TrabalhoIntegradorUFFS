from django.contrib import admin
from apps.login.models import *
# Register your models here.


class listarFiliais(admin.ModelAdmin):
    list_display = ("codfilial", "dtinclusao", "dtencerramento",
                    "cnpj", "status", "nivelfilial", "codlocal")
    list_display_links = ("codfilial", "cnpj")


admin.site.register(Filial, listarFiliais)


class listarLocalidades(admin.ModelAdmin):
    list_display = ("codlocal", "cidade", "estado")
    list_display_links = ("codlocal", "cidade")
    search_fields = ("cidade",)


admin.site.register(Localidade, listarLocalidades)


class listarMetasFiliais(admin.ModelAdmin):
    list_display = ("nivelfilial", "vigencia", "bonvendedor", "bongerente")


admin.site.register(Metafilial, listarMetasFiliais)


class listarMetasVendedores(admin.ModelAdmin):
    list_display = ("nivelvendedor", "vigencia", "pctgmeta", "bonificacao")
    list_display_links = ("nivelvendedor", "vigencia")


admin.site.register(Metavendedor, listarMetasVendedores)


class listarNiveisFiliais(admin.ModelAdmin):
    list_display = ("nivelfilial", "descricao")


admin.site.register(Nivelfilial, listarNiveisFiliais)


class listarNiveisVendedores(admin.ModelAdmin):
    list_display = ("nivelvendedor", "descricao")


admin.site.register(Nivelvendedor, listarNiveisVendedores)


class listarUsuarios(admin.ModelAdmin):
    list_display = ("codusuario", "nome", "cpf", "login", "senha", "status",
                    "dtinclusao", "dtencerramento", "tipo", "filial", "nivelvendedor")
    list_display_links = ("codusuario", "nome")


admin.site.register(Usuario, listarUsuarios)


class listarVendas(admin.ModelAdmin):
    list_display = ("codvendedor", "datavenda", "valorfaturado", "filial")


admin.site.register(Venda, listarVendas)
