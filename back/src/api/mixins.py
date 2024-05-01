from itertools import chain

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, resources, serializers


class DivisionActionMixin:

    def get_division_ids_qs(self, pk: int):
        raise NotImplementedError()

    @extend_schema(
        responses=resources.GET_SUCCESS_EMPLOYEE_STATS,
    )
    @action(detail=True, methods=['get'])
    def stat(self, request, pk):
        division_ids_qs = self.get_division_ids_qs(pk)
        division_ids = set(chain.from_iterable(division_ids_qs))
        division_ids.discard(None)
        stat = (
            models.EmployeeDivision
            .objects.filter(division_id__in=division_ids)
            .prefetch_related('employee')
            .employee_stat())
        serializer = serializers.EmployeeStatSerializer(data=stat)
        serializer.is_valid()
        return Response(serializer.data)
