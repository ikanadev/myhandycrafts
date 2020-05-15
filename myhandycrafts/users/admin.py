"""User models admin."""

# Django

# Models
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

# Models
from myhandycrafts.users.models import User, Profile



class CustomUserAdmin(UserAdmin):
    """User model admin."""
    # fields = ('email',
    #           'username',
    #           'first_name',
    #           'last_name',
    #           'is_staff',
    #           'active',
    #           'is_active',
    #           )
    list_display = ('email',
                    'username',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'active',
                    'is_active',
                    )
    # list_filter = ('is_staff','active')


    # change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

        (_('Audit info'), {'fields': ('active', )}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2'),
    #     }),
    # )



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'reputation')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


admin.site.register(User, CustomUserAdmin)

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
