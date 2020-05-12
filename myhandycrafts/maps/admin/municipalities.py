"""Municipality model admin."""
# Django
from django.contrib import admin

# models
from myhandycrafts.maps.models import Municipality


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    """Municipality model admin."""


    fields= ('name',
             'description',
             'active',
             'departament',
             'province',
            )

    list_display = ('name',
                    'description',
                    'active',
                    'departament',
                    'province',
                    )

    list_filter = ('active',
                   'departament',
                   'province',)

    search_fields = ('name',
                    'description',
                     )

