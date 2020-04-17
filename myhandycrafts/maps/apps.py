"""maps appconfig"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MapsConfig(AppConfig):
    """ config for maps of country"""
    name =  "myhandycrafts.maps"
    verbose_name = _("Maps")

