from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = "账户/权限"

    def ready(self):
        # overriding the ready method
        # This will trigger the @receiver decorator
        # and thus connect the signals
        import account.signals
