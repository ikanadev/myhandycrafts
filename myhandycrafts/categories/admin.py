"""Categories models admin."""

# Django

# Models
# Django
from django.contrib import admin


# Models
from myhandycrafts.categories.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Categorie model admin."""


    fields= ('name',
             'description',
             'active',
            )

    list_display = ('name',
                    'description',
                    'count_post',
                    'count_craftman',
                    'active',
                    )

    list_filter = ('active',)

    search_fields = ('name',
                    'description')




# admin.site.register(User, CustomUserAdmin)

# from django.contrib.auth import get_user_model
#
# from myhandycrafts.users.forms import UserChangeForm, UserCreationForm
#
# User = get_user_model()
#
#
# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#
#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
#     list_display = ["username", "name", "is_superuser"]
#     search_fields = ["name"]
