from django.apps import AppConfig


class WmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WMS'
    verbose_name = "仓储系统"

    def ready(self):
        # overriding the ready method
        # This will trigger the @receiver decorator
        # and thus connect the signals
        import WMS.signals
