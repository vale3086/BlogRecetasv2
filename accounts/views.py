from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import RegistroForm, UserUpdateForm, ProfileUpdateForm, CambiarPasswordForm
from .models import UserProfile


# ─── LOGIN (FBV) ─────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenida/o, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'accounts/login.html')


# ─── LOGOUT (FBV con decorador) ───────────────────────────────────────────────

@login_required
def logout_view(request):
    """Vista de logout - usa decorador @login_required"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')


# ─── REGISTRO (FBV) ──────────────────────────────────────────────────────────

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenida/o.')
            return redirect('home')
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})


# ─── PERFIL (CBV con LoginRequiredMixin) ──────────────────────────────────────

class PerfilView(LoginRequiredMixin, TemplateView):
    """Vista de perfil - CBV con mixin"""
    template_name = 'accounts/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil'] = self.request.user.perfil
        return context


# ─── EDITAR PERFIL (CBV con LoginRequiredMixin) ───────────────────────────────

class PerfilEditarView(LoginRequiredMixin, TemplateView):
    """Vista de edición de perfil - CBV con mixin"""
    template_name = 'accounts/perfil_editar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.perfil)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Corregí los errores del formulario.')
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form,
            })


# ─── CAMBIAR PASSWORD (FBV con decorador) ─────────────────────────────────────

@login_required
def cambiar_password_view(request):
    """Cambio de contraseña - FBV con @login_required (decorador)"""
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Corregí los errores.')
    else:
        form = CambiarPasswordForm(request.user)

    return render(request, 'accounts/cambiar_password.html', {'form': form})
