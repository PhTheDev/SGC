import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect

from .models import Chamado

@receiver(pre_save, sender=Chamado)
def pre_save_gerar_protocolo(sender, instance, **Kwargs):
    if not instance.protocolo:
        instance.protocolo = str(uuid.uuid4())[:8].upper()


@receiver(user_logged_in)
def redirect_superuser(sender, user, request, **kwargs):
    if user.is_superuser:
        return redirect('inicio')
    else:
        return redirect('colaborador')