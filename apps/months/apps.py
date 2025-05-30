from django.apps import AppConfig


class MonthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.months'
    verbose_name = "Месяца и Оплаты"

    def ready(self):
        import apps.months.signals
