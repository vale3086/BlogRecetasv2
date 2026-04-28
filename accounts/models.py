from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    biografia = models.TextField(blank=True, verbose_name='Biografía')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')
    link = models.URLField(blank=True, verbose_name='Sitio web / Link')

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


# Auto-crear perfil al crear un User
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(usuario=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
