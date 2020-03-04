from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesConfig(AppConfig):
    name = "myhandycrafts.categories"
    verbose_name = _("Categories")

    # def ready(self):
    #     try:
    #         import myhandycrafts.users.signals  # noqa F401
    #     except ImportError:
    #         pass
