from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.views.generic import TemplateView
from django.conf.urls import handler500

# Importe sua função handler404
from app_sgc.views import handler404

# Configuração dos handlers
handler404 = handler404

handler500 = 'app_sgc.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_sgc.urls')),
    path('accounts/', include('allauth.urls')),
    path('usuarios/', include('users.urls')),
]
