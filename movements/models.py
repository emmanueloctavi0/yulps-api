from django.db import models
from django.contrib.auth import get_user_model

from core.models import AbstractBaseModel


class MovementCategory(AbstractBaseModel):
    """Modelo para las categorias de los movimientos"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """Regresa el nombre de la categoria"""
        return self.name


class Movement(AbstractBaseModel):
    """Modelo de un movimiento financiero"""
    detail = models.CharField(max_length=255)
    mount = models.FloatField()
    is_entry = models.BooleanField(default=False)
    iso_code = models.CharField(max_length=50, default='MXN')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(MovementCategory, on_delete=models.DO_NOTHING)

    def __str__(self):
        """Regresa el detalle con la cantidad"""
        return '{} - ${}{}'.format(self.detail, self.mount, self.iso_code)
