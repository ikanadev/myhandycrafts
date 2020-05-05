"""fairs appconfig"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FairsConfig(AppConfig):
    """ config for fairs"""
    name =  "myhandycrafts.fairs"
    verbose_name = _("Fairs")

