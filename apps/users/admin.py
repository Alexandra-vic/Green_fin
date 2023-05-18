from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': (
            'full_name',
            'brigades_name',
            'brigades_list',
            'company_name',
            'address',
            'phone',
    
        )}),
        ('Permissions', {'fields': (
            'is_operator',
            'is_brigade',
            'is_client',
        )}),
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
    )


# class OperatorAdmin(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'full_name',
#         'password',
#     )


# class BrigadeAdmin(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'brigades_name',
#         'brigades_list',
#         'password',
#     )


# class ClientAdmin(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'company_name',
#         'address',
#         'phone',
#         'password',
#     )


admin.site.register(User, UserAdmin)
# admin.site.register(User, OperatorAdmin)
# admin.site.register(User, BrigadeAdmin)
# admin.site.register(User, ClientAdmin)
