from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Cuentas y Perfiles'

    def ready(self):
        import accounts.models  # activa las señales
