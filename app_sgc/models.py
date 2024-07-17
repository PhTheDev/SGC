import uuid
from django.db import models
from stdimage.models import StdImageField
from .choices import Locais, StatusChamado
from datetime import datetime
from django.contrib.auth.models import User


# Definição de modelos referenciados, se não existirem
class NomeUsuario(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NomeDepartamento(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NomeProfile(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MotivoChamado(models.Model):
    motivo = models.CharField('Motivo Chamado', max_length=50)

    class Meta:
        verbose_name = 'Motivo Chamado'
        verbose_name_plural = 'Motivos Chamado'

    def __str__(self):
        return self.motivo


# Classe base para adicionar campos de criação e modificação a outros modelos
class Base(models.Model):
    criado = models.DateField('Criacao', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)

    class Meta:
        abstract = True


# Função para gerar um caminho de arquivo único para as imagens, evitando colisão de nome
def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


# Classe para lidar com imagens associadas a um "Chamado"
class ImagemChamado(models.Model):
    imagem = StdImageField('Imagem', upload_to=get_file_path, null=True, blank=True)

    def __str__(self):
        return self.imagem.name

    @property
    def nome_imagem(self):
        return self.imagem.name.split('/')[-1]


# Classe para lidar com usuários
class Usuario(Base):
    nome_usuario = models.ForeignKey(NomeUsuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return str(self.nome_usuario)


# Classe para lidar com departamentos
class Departamento(Base):
    nome_departamento = models.ForeignKey(NomeDepartamento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return str(self.nome_departamento)


# Classe para lidar com perfis
class Profile(Base):
    nome_profile = models.ForeignKey(NomeProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username} - {self.get_perfil_display()}'


# Classe para lidar com "Chamado" (ticket)
class Chamado(Base):
    protocolo = models.CharField('Protocolo', max_length=50, unique=True)
    assunto_chamado = models.TextField('Assunto', max_length=500)
    relato_chamado = models.TextField('Relato Chamado', max_length=500)
    motivo_chamado = models.ManyToManyField(MotivoChamado, verbose_name='Motivo do Chamado')
    data_hora_chamado = models.DateTimeField('Data e Hora do Chamado', default=datetime.now)
    relato_suporte = models.TextField('Relato suporte', max_length=500)
    data_hora_finalizado = models.DateTimeField('Data e Hora de Finalização', default=datetime.now)
    envia_avisos = models.EmailField('Email', max_length=500)
    imagem_chamado = models.ManyToManyField(ImagemChamado, blank=True)
    prazo = models.DateTimeField('Prazo', null=True, blank=True)
    local_suporte = models.CharField(max_length=50, choices=Locais.choices)
    status_chamado = models.CharField(max_length=50, choices=StatusChamado.choices, default=StatusChamado.RECEBIDA)
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chamados_criados', null=True)

    def __str__(self):
        return f"{self.assunto_chamado} - {self.relato_chamado}"

    # Método para obter os motivos do "Chamado"
    def get_motivo_chamado(self):
        return ', '.join([motivo.motivo for motivo in self.motivo_chamado.all()])

    get_motivo_chamado.short_description = 'Motivo do Chamado'

    class Meta:
        verbose_name = 'Chamado'
        verbose_name_plural = 'Chamados'
