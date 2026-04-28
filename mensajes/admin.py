from django.contrib import admin
from .models import Mensaje


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('remitente', 'destinatario', 'asunto', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('asunto', 'remitente__username', 'destinatario__username')
    readonly_fields = ('fecha_envio',)
