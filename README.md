# BlogRecetas-Castillo

Blog de recetas desarrollado con **Django** como proyecto final del curso de CoderHouse.

**Autora:** Valeria Castillo  
**Repositorio:** `TuPrimeraPaginaFinal-Castillo`  
**Demo:** https://www.loom.com/share/2cb5aaad856a42b4b51dd121441a5de6 

---

## Tecnologías

- Python 3.10+
- Django 4.2
- SQLite (base de datos local)
- Bootstrap 5.3 (estilos via CDN)
- CKEditor (editor de texto enriquecido)
- Pillow (manejo de imágenes)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TuPrimeraPaginaFinal-Castillo.git
cd TuPrimeraPaginaFinal-Castillo
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (para el admin)

```bash
python manage.py createsuperuser
```

### 6. Correr el servidor

```bash
python manage.py runserver
```

Abrí el navegador en **http://127.0.0.1:8000/**

---

## Orden para probar las funcionalidades

| Paso | URL | Descripción |
|------|-----|-------------|
| 1 | `/` | Página de inicio / Home |
| 2 | `/about/` | Acerca de mí |
| 3 | `/accounts/registro/` | Crear cuenta de usuario |
| 4 | `/accounts/login/` | Iniciar sesión |
| 5 | `/pages/` | Listado de recetas (buscar desde acá) |
| 6 | `/pages/crear/` | Crear nueva receta (requiere login) |
| 7 | `/pages/<pk>/` | Ver detalle de una receta |
| 8 | `/pages/<pk>/editar/` | Editar receta (requiere ser autor) |
| 9 | `/pages/<pk>/eliminar/` | Eliminar receta (requiere ser autor) |
| 10 | `/accounts/perfil/` | Ver mi perfil |
| 11 | `/accounts/perfil/editar/` | Editar perfil y avatar |
| 12 | `/accounts/perfil/cambiar-password/` | Cambiar contraseña |
| 13 | `/mensajes/` | Bandeja de mensajes |
| 14 | `/mensajes/enviar/` | Enviar mensaje a otro usuario |
| 15 | `/admin/` | Panel de administración (superusuario) |

---

## Estructura del proyecto

```
TuPrimeraPaginaFinal-Castillo/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── blogrecetas/               # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pages/                     # App principal - recetas/blog
│   ├── models.py              # Modelo Receta
│   ├── forms.py               # RecetaForm, BuscarRecetaForm
│   ├── views.py               # CBVs: HomeView, AboutView, RecetaListView, etc.
│   ├── urls.py
│   ├── admin.py
│   └── templates/pages/
│       ├── base.html          # Template base (herencia)
│       ├── home.html
│       ├── about.html
│       ├── receta_list.html
│       ├── receta_detail.html
│       ├── receta_form.html
│       └── receta_confirm_delete.html
├── accounts/                  # App de autenticación y perfiles
│   ├── models.py              # Modelo UserProfile
│   ├── forms.py               # RegistroForm, UserUpdateForm, ProfileUpdateForm
│   ├── views.py               # login, logout, registro, PerfilView, etc.
│   ├── urls.py
│   ├── admin.py
│   └── templates/accounts/
│       ├── login.html
│       ├── registro.html
│       ├── perfil.html
│       ├── perfil_editar.html
│       └── cambiar_password.html
└── mensajes/                  # App de mensajería
    ├── models.py              # Modelo Mensaje
    ├── forms.py               # MensajeForm
    ├── views.py               # BandejaView, MensajeDetailView, enviar_mensaje_view
    ├── urls.py
    ├── admin.py
    └── templates/mensajes/
        ├── bandeja.html
        ├── enviar.html
        └── detalle.html
```

---

## Modelos

- **Receta** (pages): titulo, subtitulo, contenido (RichTextField/CKEditor), imagen, fecha, autor, dificultad, tiempo_preparacion
- **UserProfile** (accounts): usuario (OneToOne), avatar, biografia, fecha_nacimiento, link
- **Mensaje** (mensajes): remitente, destinatario, asunto, cuerpo, fecha_envio, leido

## Vistas (patrón MVT)

### Clases basadas en vista (CBV) con mixins:
- `HomeView` (TemplateView)
- `AboutView` (TemplateView)
- `RecetaListView` (ListView)
- `RecetaDetailView` (DetailView)
- `RecetaCreateView` (CreateView + **LoginRequiredMixin**)
- `RecetaUpdateView` (UpdateView + **LoginRequiredMixin**)
- `RecetaDeleteView` (DeleteView + **LoginRequiredMixin**)
- `PerfilView` (TemplateView + **LoginRequiredMixin**)
- `PerfilEditarView` (TemplateView + **LoginRequiredMixin**)
- `BandejaView` (ListView + **LoginRequiredMixin**)
- `MensajeDetailView` (DetailView + **LoginRequiredMixin**)

### Vistas con decoradores:
- `logout_view` (**@login_required**)
- `cambiar_password_view` (**@login_required**)
- `enviar_mensaje_view` (**@login_required**)

## Herencia de templates

Todos los templates heredan de `pages/base.html` usando `{% extends 'pages/base.html' %}`. El base incluye el navbar completo con acceso a Inicio, Recetas, Acerca de mí, Mensajes, Perfil, Login/Registro y Logout.
