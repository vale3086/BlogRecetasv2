from django.contrib import admin
from .models import Receta


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'dificultad', 'tiempo_preparacion', 'fecha')
    search_fields = ('titulo', 'subtitulo')
    list_filter = ('dificultad', 'autor', 'fecha')
    readonly_fields = ('fecha',)
