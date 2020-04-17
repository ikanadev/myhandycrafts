from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoresConfig(AppConfig):
    name = "myhandycrafts.stores"
    verbose_name = _("Stores")