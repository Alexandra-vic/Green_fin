from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User, Operator, Brigade, Client


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'role', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', )
    search_fields = ('full_name',)


@admin.register(Brigade)
class BrigadeAdmin(admin.ModelAdmin):
    list_display = ('name', 'members', )
    search_fields = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name', 'address', 'phone', )
    search_fields = ('company_name',)
