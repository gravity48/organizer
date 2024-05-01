import api.models
from api import models as api_models

from .base import ModelLayer


class ServiceLayer(ModelLayer):
    """Слой службы."""

    model = api_models.Service


class AdministrationLayer(ModelLayer):
    """Слой управления."""

    model = api.models.Administration
    related_name = 'administrations'


class DepartmentLayer(ModelLayer):
    """Слой отдела."""

    model = api_models.Department
    related_name = 'departments'


class GroupLayer(ModelLayer):
    """Слой группы."""

    model = api_models.Group
    related_name = 'groups'
