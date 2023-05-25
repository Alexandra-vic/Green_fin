from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User


class UsersAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': (
            'full_name',
            'brigades_name',
            'brigades_list',
            'company_name',
            'address',
            'phone',
            'user_type',

        )}),
        # ('Permissions', {'fields': (
        #     'is_operator',
        #     'is_brigade',
        #     'is_client'
        # )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = (
        'email',
        'full_name',
        'brigades_name',
        'brigades_list',
        'company_name',
        'address',
        'phone',
        'user_type',
    )


admin.site.register(User, UserAdmin)
