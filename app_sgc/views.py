from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import make_aware
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .decorators import dti_required, colaborador_required
from .choices import Locais
from .models import Chamado, ImagemChamado, MotivoChamado, StatusChamado

# Requer login e autorização de colaborador
@login_required
@colaborador_required
def Index(request):
    # Renderiza a página inicial para colaboradores
    return render(request, 'app_sgc/index.html')


# Requer login e autorização de DTI
@login_required
@dti_required
def Inicio(request):
    # Renderiza a página de início para DTI
    return render(request, 'app_sgc/inicio.html')


# Requer login e autorização de DTI
@login_required
@dti_required
def Reports(request):
    # Renderiza a página de relatórios
    return render(request, 'app_sgc/reports.html')


# Requer login e autorização de DTI
@login_required
@dti_required
def Recebidos(request):
    if request.method == 'POST':
        # Captura dados do formulário
        protocolo = request.POST.get('protocolo')
        relato_suporte = request.POST.get('relatosuporte')
        prazo = request.POST.get('prazo')
        submit_button = request.POST.get('submit_button')

        # Busca o chamado pelo protocolo
        chamado = Chamado.objects.filter(protocolo=protocolo).first()

        if chamado:
            # Atualiza os campos do chamado
            chamado.relato_suporte = relato_suporte
            chamado.prazo = prazo

            # Atualiza o status do chamado com base no botão clicado
            if submit_button == 'finalizar':
                chamado.status_chamado = StatusChamado.FINALIZADO
            elif submit_button == 'salvar':
                chamado.status_chamado = StatusChamado.ANALISE

            # Salva as alterações no chamado
            chamado.save()

        # Redireciona para a mesma página para exibir os chamados atualizados
        return HttpResponseRedirect(reverse('recebidos'))

    else:
        # Se não for um POST, exibe a página com os chamados recebidos
        context = {
            'chamados': Chamado.objects.filter(status_chamado=StatusChamado.RECEBIDA)
        }
        return render(request, 'app_sgc/recebidos.html', context)
    

# Requer login e autorização de DTI
@login_required
@dti_required
def EmAnalize(request):
    if request.method == 'POST':
        # Captura dados do formulário
        protocolo = request.POST.get('protocolo')
        relatosuporte = request.POST.get('relatosuporte')
        prazo_str = request.POST.get('prazo')
        action = request.POST.get('action')

        try:
            # Converte a string do prazo para um objeto datetime e ajusta para o fuso horário correto
            prazo = datetime.fromisoformat(prazo_str)
            prazo = make_aware(prazo)

            # Busca o chamado pelo protocolo
            chamado = Chamado.objects.filter(protocolo=protocolo).first()

            if chamado:
                # Atualiza os campos do chamado
                chamado.relato_suporte = relatosuporte
                chamado.prazo = prazo

                # Atualiza o status do chamado se a ação for finalizar
                if action == 'finalizar':
                    chamado.status_chamado = 'F'

                # Salva as alterações no chamado
                chamado.save()

                # Exibe uma mensagem de sucesso e redireciona para a página de espera
                messages.success(request, "Chamado Finalizado com sucesso!")
                return redirect('espera')
            else:
                # Exibe uma mensagem de erro se o chamado não for encontrado
                messages.error(request, "Chamado não encontrado!")

        except Exception as e:
            # Exibe uma mensagem de erro se ocorrer uma exceção
            messages.error(request, f"Ocorreu um erro ao atualizar o chamado: {str(e)}")

    # Renderiza a página com os chamados em análise
    context = {
        'chamados': Chamado.objects.filter(status_chamado='A')
    }
    return render(request, 'app_sgc/espera.html', context)


# Requer login e autorização de DTI
@login_required
@dti_required
def Finalizados(request):
    # Renderiza a página com os chamados finalizados
    context = {
        'chamados': Chamado.objects.all().filter(status_chamado='F' or StatusChamado.FINALIZADO)
    }
    return render(request, 'app_sgc/finalizados.html', context)


# Requer login e autorização de colaborador
@login_required
@colaborador_required
def FinalizadosColaborador(request):
    # Renderiza a página com os chamados finalizados criados pelo colaborador
    context = {
        'chamados': Chamado.objects.all().filter(status_chamado=StatusChamado.FINALIZADO, usuario_criacao=request.user)
    }
    return render(request, 'app_sgc/finalizadoscolaborador.html', context)


# Requer login e autorização de DTI
@login_required
@dti_required
def Motivos(request):
    # Renderiza a página com os motivos de chamados
    return render(request, 'app_sgc/motivos.html')


# Requer login e autorização de colaborador
@login_required
@colaborador_required
def Colaborador(request):
    # Renderiza a página principal para colaboradores
    return render(request, 'app_sgc/colaborador.html')


# Requer login e autorização de colaborador
@login_required
@colaborador_required
def NovoChamado(request):
    if request.method == 'POST':
        # Captura dados do formulário
        assuntochamado = request.POST.get('assuntochamado')
        relatochamado = request.POST.get('relatochamado')
        localatendimento = request.POST.get('localatendimento')
        motivos = request.POST.getlist('motivos')
        arquivos = request.FILES.getlist('fileUpload[]')

        # Cria um novo chamado
        chamado = Chamado.objects.create(
            assunto_chamado=assuntochamado,
            relato_chamado=relatochamado,
            local_suporte=localatendimento,
            status_chamado='R',
            usuario_criacao=request.user,
        )

        # Adiciona os motivos ao chamado
        for motivo_id in motivos:
            try:
                motivo = MotivoChamado.objects.get(id=motivo_id)
                chamado.motivo_chamado.add(motivo)
            except MotivoChamado.DoesNotExist:
                pass

        # Salva as imagens do chamado
        for arquivo in arquivos:
            img = ImagemChamado.objects.create(imagem=arquivo)
            chamado.imagem_chamado.add(img)

        # Exibe uma mensagem de sucesso e redireciona para a página de novo chamado
        messages.success(request, "Chamado Realizado com sucesso!")
        return redirect('novo_chamado')

    # Renderiza a página para criação de novo chamado com motivos e locais de atendimento
    MOTIVOS_CHAMADOS = MotivoChamado.objects.all()
    context = {
        'motivos': MOTIVOS_CHAMADOS,
        'locais': Locais.choices
    }
    return render(request, 'app_sgc/novo_chamado.html', context)


# Requer login e autorização de colaborador
@login_required
@colaborador_required
def Realizados(request):
    # Renderiza a página com os chamados realizados pelo colaborador
    context = {
        'chamados': Chamado.objects.filter(
            usuario_criacao=request.user
        ).filter(
            Q(status_chamado=StatusChamado.ANALISE) | Q(status_chamado=StatusChamado.RECEBIDA)
        )
    }
    return render(request, 'app_sgc/realizados.html', context)


def handler404(request, exception):
    return render(request, 'app_sgc/404.html', status=404)


def custom_500(request):
    return render(request, 'app_sgc/500.html', status=500)