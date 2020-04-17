"""Maps contry model.

This module is building for Bolivia country.
"""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel


class Province(MyHandycraftsModel):
    """Province model.

    Province models is a subdivision of departament.
    """
    departament = models.ForeignKey(
        'maps.Departament',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name

