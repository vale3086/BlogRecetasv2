from django import forms
from django.contrib.auth.models import User
from .models import Mensaje


class MensajeForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Destinatario',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Mensaje
        fields = ['destinatario', 'asunto', 'cuerpo']
        labels = {
            'asunto': 'Asunto',
            'cuerpo': 'Mensaje',
        }
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mensaje'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribí tu mensaje...'}),
        }
