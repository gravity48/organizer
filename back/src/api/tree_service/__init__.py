import enum

from .base import TreeFactory
from .layers import AdministrationLayer, DepartmentLayer, GroupLayer, ServiceLayer


class SourcesEnum(str, enum.Enum):
    """Enum источников."""

    ROOT = 'root'
    SERVICE = 'service'
    ADMINISTRATION = 'administration'
    DEPARTMENT = 'department'
    GROUP = 'group'

    @classmethod
    def values(cls):
        return list(map(lambda field: field.value, cls))


service_layer = ServiceLayer(SourcesEnum.SERVICE.value)
administration_layer = AdministrationLayer(SourcesEnum.ADMINISTRATION.value)
department_layer = DepartmentLayer(SourcesEnum.DEPARTMENT.value)
group_layer = GroupLayer(SourcesEnum.GROUP.value)

service_tree = TreeFactory('Подразделения')
service_tree.add_layer(service_layer)
service_tree.add_layer(administration_layer)
service_tree.add_layer(department_layer)
service_tree.add_layer(group_layer)
