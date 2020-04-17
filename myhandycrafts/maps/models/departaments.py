"""Maps contry model.

This module is building for Bolivia country.
"""

# Django
from django.db import models

# Utils
from myhandycrafts.utils.models import MyHandycraftsModel


class Departament(MyHandycraftsModel):
    """Departament model.

    Departament model is a division from country
    """


    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256,blank=True)

    def __str__(self):
        return self.name



