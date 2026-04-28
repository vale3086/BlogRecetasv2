from django import forms
from .models import Receta


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'subtitulo', 'contenido', 'imagen', 'dificultad', 'tiempo_preparacion']
        labels = {
            'titulo': 'Título',
            'subtitulo': 'Subtítulo / Descripción breve',
            'contenido': 'Contenido / Instrucciones',
            'imagen': 'Imagen de la receta',
            'dificultad': 'Dificultad',
            'tiempo_preparacion': 'Tiempo de preparación (minutos)',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Torta de chocolate casera'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Una breve descripción de la receta'}),
            'dificultad': forms.Select(attrs={'class': 'form-select'}),
            'tiempo_preparacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class BuscarRecetaForm(forms.Form):
    q = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título o descripción...',
        })
    )
