from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('media', 'Media'),
        ('dificil', 'Difícil'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    subtitulo = models.CharField(max_length=300, verbose_name='Subtítulo / Descripción breve')
    contenido = RichTextField(verbose_name='Contenido / Instrucciones')
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True, verbose_name='Imagen')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha de publicación')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas', verbose_name='Autor')
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default='facil', verbose_name='Dificultad')
    tiempo_preparacion = models.PositiveIntegerField(default=30, verbose_name='Tiempo de preparación (min)')

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo
