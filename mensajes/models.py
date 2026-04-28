from django.db import models
from django.contrib.auth.models import User


class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados', verbose_name='Remitente')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos', verbose_name='Destinatario')
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    cuerpo = models.TextField(verbose_name='Mensaje')
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de envío')
    leido = models.BooleanField(default=False, verbose_name='Leído')

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f'De {self.remitente} a {self.destinatario}: {self.asunto}'
