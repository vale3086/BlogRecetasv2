from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

from .models import Receta
from .forms import RecetaForm, BuscarRecetaForm


# ─── HOME ────────────────────────────────────────────────────────────────────

class HomeView(TemplateView):
    """Vista de inicio - CBV"""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimas_recetas'] = Receta.objects.select_related('autor').all()[:6]
        return context


# ─── ABOUT ───────────────────────────────────────────────────────────────────

class AboutView(TemplateView):
    """Vista 'Acerca de mí' - CBV - route: about/"""
    template_name = 'pages/about.html'


# ─── RECETAS (PAGES) ─────────────────────────────────────────────────────────

class RecetaListView(ListView):
    """Listado de recetas con búsqueda - CBV - route: pages/"""
    model = Receta
    template_name = 'pages/receta_list.html'
    context_object_name = 'recetas'
    paginate_by = 6

    def get_queryset(self):
        qs = Receta.objects.select_related('autor').all()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(subtitulo__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busqueda'] = BuscarRecetaForm(self.request.GET or None)
        context['query'] = self.request.GET.get('q', '')
        return context


class RecetaDetailView(DetailView):
    """Detalle de una receta - CBV - route: pages/<pk>/"""
    model = Receta
    template_name = 'pages/receta_detail.html'
    context_object_name = 'receta'


class RecetaCreateView(LoginRequiredMixin, CreateView):
    """Crear receta - CBV con LoginRequiredMixin"""
    model = Receta
    form_class = RecetaForm
    template_name = 'pages/receta_form.html'
    success_url = reverse_lazy('receta_list')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'Receta creada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = 'Nueva Receta'
        context['accion'] = 'Crear'
        return context


class RecetaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar receta - CBV con LoginRequiredMixin"""
    model = Receta
    form_class = RecetaForm
    template_name = 'pages/receta_form.html'
    success_url = reverse_lazy('receta_list')

    def dispatch(self, request, *args, **kwargs):
        receta = self.get_object()
        if receta.autor != request.user and not request.user.is_staff:
            messages.error(request, 'No tenés permiso para editar esta receta.')
            return redirect('receta_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Receta actualizada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = 'Editar Receta'
        context['accion'] = 'Guardar cambios'
        return context


class RecetaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar receta - CBV con LoginRequiredMixin"""
    model = Receta
    template_name = 'pages/receta_confirm_delete.html'
    success_url = reverse_lazy('receta_list')
    context_object_name = 'receta'

    def dispatch(self, request, *args, **kwargs):
        receta = self.get_object()
        if receta.autor != request.user and not request.user.is_staff:
            messages.error(request, 'No tenés permiso para eliminar esta receta.')
            return redirect('receta_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Receta eliminada.')
        return super().form_valid(form)
