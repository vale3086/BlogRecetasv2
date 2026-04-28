from django.urls import path
from .views import login_view, logout_view, registro_view, PerfilView, PerfilEditarView, cambiar_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro_view, name='registro'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', PerfilEditarView.as_view(), name='perfil_editar'),
    path('perfil/cambiar-password/', cambiar_password_view, name='cambiar_password'),
]
