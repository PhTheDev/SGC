from django.contrib import admin
from .models import Chamado, Usuario, Departamento, Profile, NomeUsuario, NomeDepartamento, NomeProfile, MotivoChamado


@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario',)
    search_fields = ['nome_usuario__name']
    autocomplete_fields = ['nome_usuario']


@admin.register(Departamento)
class DepartamentosAdmin(admin.ModelAdmin):
    list_display = ('nome_departamento',)
    search_fields = ['nome_departamento__name']
    autocomplete_fields = ['nome_departamento']


@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('nome_profile',)
    search_fields = ['nome_profile__name']
    autocomplete_fields = ['nome_profile']


@admin.register(MotivoChamado)
class MotivosAdmin(admin.ModelAdmin):
    list_display = ('motivo',)


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('assunto_chamado', 'relato_chamado', 'get_motivo_chamado', 'data_hora_chamado',
                    'relato_suporte', 'data_hora_finalizado', 'envia_avisos',
                    'prazo', 'local_suporte', 'status_chamado', 'get_imagem_chamados'
                    )

    def get_imagem_chamados(self, obj):
        return ", ".join([imagem.nome_imagem for imagem in obj.imagem_chamado.all()])

    get_imagem_chamados.short_description = 'Imagem Chamados'


@admin.register(NomeUsuario)
class NomeUsuarioAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(NomeDepartamento)
class NomeDepartamentoAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(NomeProfile)
class NomeProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']

