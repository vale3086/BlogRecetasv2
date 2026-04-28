from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_nacimiento', 'link')
    search_fields = ('usuario__username', 'usuario__email')
    raw_id_fields = ('usuario',)
