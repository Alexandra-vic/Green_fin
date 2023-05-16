from django.contrib import admin
from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
            'email', 'full_name', 'is_admin', )

    search_fields = ('full_name',)
