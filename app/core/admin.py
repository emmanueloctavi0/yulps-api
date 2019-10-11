from django.contrib import admin
from django.contrib.auth import get_user_model


class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_staff', 'is_superuser',)
    fields = (
        ('email', 'last_login',),
        ('first_name', 'last_name',),
        ('is_staff', 'is_superuser', 'is_active',),
        ('groups',),
        ('created_at', 'updated_at',),
        ('password',),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login',)


admin.site.register(get_user_model(), AdminUser)
