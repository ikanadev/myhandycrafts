"""Province model admin."""
# Django
from django.contrib import admin

# models
from myhandycrafts.maps.models import Province


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """Province model admin."""


    fields= (
             'departament',
             'name',
             'description',
             'active',
            )

    list_display = ('name',
                    'description',
                    'active',
                    'departament',
                    )

    list_filter = ('active','departament',)

    search_fields = ('name',
                    'description',
                     )

