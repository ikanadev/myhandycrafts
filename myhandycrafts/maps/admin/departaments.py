"""Departament model admin."""
# Django
from django.contrib import admin

# models
from myhandycrafts.maps.models import Departament


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    """Departament model admin."""


    fields= ('name',
             'description',
             'active',
            )

    list_display = ('name',
                    'description',
                    'active',
                    )

    list_filter = ('active',)

    search_fields = ('name',
                    'description',
                     )

