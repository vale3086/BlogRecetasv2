from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Mensaje
from .forms import MensajeForm


# ─── BANDEJA DE ENTRADA (CBV con LoginRequiredMixin) ─────────────────────────

class BandejaView(LoginRequiredMixin, ListView):
    """Bandeja de entrada - CBV con mixin"""
    model = Mensaje
    template_name = 'mensajes/bandeja.html'
    context_object_name = 'mensajes_recibidos'

    def get_queryset(self):
        return Mensaje.objects.filter(
            destinatario=self.request.user
        ).select_related('remitente').order_by('-fecha_envio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensajes_enviados'] = Mensaje.objects.filter(
            remitente=self.request.user
        ).select_related('destinatario').order_by('-fecha_envio')
        context['no_leidos'] = self.get_queryset().filter(leido=False).count()
        return context


# ─── DETALLE DE MENSAJE (CBV con LoginRequiredMixin) ─────────────────────────

class MensajeDetailView(LoginRequiredMixin, DetailView):
    """Detalle de mensaje - CBV con mixin"""
    model = Mensaje
    template_name = 'mensajes/detalle.html'
    context_object_name = 'mensaje'

    def get_object(self):
        obj = get_object_or_404(Mensaje, pk=self.kwargs['pk'])
        # Solo el remitente o destinatario pueden ver el mensaje
        if obj.destinatario != self.request.user and obj.remitente != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        # Marcar como leído si es el destinatario
        if obj.destinatario == self.request.user and not obj.leido:
            obj.leido = True
            obj.save()
        return obj


# ─── ENVIAR MENSAJE (FBV con @login_required - decorador) ────────────────────

@login_required
def enviar_mensaje_view(request):
    """Enviar mensaje - FBV con decorador @login_required"""
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            if mensaje.destinatario == request.user:
                messages.error(request, 'No podés enviarte mensajes a vos mismo.')
            else:
                mensaje.save()
                messages.success(request, f'Mensaje enviado a {mensaje.destinatario.username}.')
                return redirect('bandeja')
    else:
        # Pre-seleccionar destinatario si viene por GET
        destinatario_id = request.GET.get('para')
        initial = {}
        if destinatario_id:
            from django.contrib.auth.models import User
            try:
                initial['destinatario'] = User.objects.get(pk=destinatario_id)
            except User.DoesNotExist:
                pass
        form = MensajeForm(initial=initial)

    return render(request, 'mensajes/enviar.html', {'form': form})
