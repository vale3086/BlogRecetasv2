from django.urls import path
from .views import BandejaView, MensajeDetailView, enviar_mensaje_view

urlpatterns = [
    path('', BandejaView.as_view(), name='bandeja'),
    path('enviar/', enviar_mensaje_view, name='enviar_mensaje'),
    path('<int:pk>/', MensajeDetailView.as_view(), name='mensaje_detalle'),
]
