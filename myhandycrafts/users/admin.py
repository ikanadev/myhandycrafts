"""User models admin."""

# Django

# Models
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from myhandycrafts.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('type_user', 'is_staff', 'created_at', 'updated_at')


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
