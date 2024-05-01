from itertools import chain

from rest_framework.filters import BaseFilterBackend

from . import models


class EmployeeDivisionFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        division_id = request.GET.get('division_id')
        if not division_id:
            return queryset
        division = models.Division.objects.filter(id=division_id).first()
        if not division:
            return queryset.none()
        division_ids_qs = (
            division.source_model
            .objects
            .filter(division_id=division_id)
            .division_ids())
        division_ids = set(chain.from_iterable(division_ids_qs))
        division_ids.discard(None)
        return queryset.filter(division__id__in=division_ids)
