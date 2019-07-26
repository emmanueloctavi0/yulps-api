from django.contrib import admin

from . import models


class AdminCategory(admin.ModelAdmin):
    """Admin para las categorias"""
    list_display = ('name', 'description',)
    fields = ('name', 'description',)


class AdminMovement(admin.ModelAdmin):
    """Admin para los movimientos"""
    list_display = ('detail', 'category', 'mount', 'iso_code','is_entry',)


admin.site.register(models.MovementCategory, AdminCategory)
admin.site.register(models.Movement, AdminMovement)
