from django.urls import path
from .views import HomeView, AboutView, RecetaListView, RecetaDetailView, RecetaCreateView, RecetaUpdateView, RecetaDeleteView

urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),

    # About (route: about/)
    path('about/', AboutView.as_view(), name='about'),

    # Pages / Recetas (route: pages/)
    path('pages/', RecetaListView.as_view(), name='receta_list'),
    path('pages/crear/', RecetaCreateView.as_view(), name='receta_crear'),
    path('pages/<int:pk>/', RecetaDetailView.as_view(), name='receta_detalle'),
    path('pages/<int:pk>/editar/', RecetaUpdateView.as_view(), name='receta_editar'),
    path('pages/<int:pk>/eliminar/', RecetaDeleteView.as_view(), name='receta_eliminar'),
]
