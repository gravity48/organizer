from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Базовая модель."""

    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
