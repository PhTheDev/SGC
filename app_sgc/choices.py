from django.db import models

class Locais(models.TextChoices):
    PLENARIO = 'Plenario', 'Plenario'
    DRH = 'Departamento de Recursos Humanos', 'Departamento de Recursos Humanos'
    DC = 'Departamento de Contabilidade', 'Departamento de Contabilidade'
    DF = 'Departamento Financeiro', 'Departamento financeiro'


class StatusChamado(models.TextChoices):
    RECEBIDA = 'R', 'Recebida'
    ANALISE = 'A', 'Analise'
    FINALIZADO = 'F', 'Finalizado'

