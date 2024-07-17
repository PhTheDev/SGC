from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('DTI/inicio', Inicio, name='inicio'),
    path('DTI/recebidos', Recebidos, name='recebidos'),
    path('DTI/espera', EmAnalize, name='espera'),
    path('DTI/finalizados', Finalizados, name='finalizados'),
    path('DTI/motivos', Motivos, name='motivos'),
    path('DTI/colaborador', Colaborador, name='colaborador'),
    path('colaborador/novo_chamado', NovoChamado, name='novo_chamado'),
    path('colaborador/realizados', Realizados, name='realizados'),
    path('colaborador/finalizados', FinalizadosColaborador, name='finalizadoscolaborador'),

]
