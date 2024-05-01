import datetime

from django.db import models
from django.db.models import Avg, Case, Count, ExpressionWrapper, Value, When
from django.db.models.functions import Coalesce, ExtractDay, ExtractYear
from django.utils.translation import gettext_lazy as _


class SourceChoices(models.TextChoices):
    SERVICE = 'SERVICE', _('Служба')
    ADMINISTRATION = 'ADMINISTRATION', _('Управления')
    DEPARTMENT = 'DEPARTMENT', _('Отдел')
    GROUP = 'GROUP', _('Группа')


class EmployeeDivisionQuerySet(models.QuerySet):
    """EmployeeDivision QuerySet."""

    def employee_exp(self):
        """Стаж сотрудника."""
        return self.annotate(
            employee_exp=ExpressionWrapper(
                ExtractDay(datetime.date.today() - models.F('start_at')),
                output_field=models.IntegerField(),
            ),
        )

    def employee_year(self):
        """Возраст сотрудника."""
        expression = ExtractYear(
            models.Func(
                datetime.date.today(), models.F('employee__birthday'),
                function='AGE',
            ),
        )
        return self.annotate(
            employee_year=ExpressionWrapper(
                expression,
                output_field=models.IntegerField(),
            ),
        )

    def employee_stat(self):
        """Статистика по сотрудникам."""
        return (
            self.employee_exp()
            .employee_year()
            .aggregate(
                employee_count=Count('id'),
                employee_avg_year=Avg(
                    'employee_year',
                    output_field=models.IntegerField(),
                ),
                employee_avg_exp=Avg(
                    'employee_exp',
                    output_field=models.IntegerField(),
                ),
            ))


class EmployeeQuerySet(models.QuerySet):
    """QuerySet сотрудников."""

    def prefetch_all(self):
        """Joins."""
        return (
            self.prefetch_related('division')
            .prefetch_related('division__service')
            .prefetch_related('division__administration')
            .prefetch_related('division__department')
            .prefetch_related('division__group')
        )

    def division_info(self):
        """Название подразделения."""
        prefix = 'division'
        titles = {
            'administration__title',
            'service__title',
            'department__title',
            'group__title',
        }
        fields = []
        for title in titles:
            fields.append(models.F(f'{prefix}__{title}'))
        return (
            self.annotate(
                division_title=Coalesce(
                    *fields,
                ),
            )
            .annotate(start_at=models.F('employeedivision__start_at'))
            .annotate(division_type=models.F('division__source')))

    def order_by_source(self):
        """Сортировка по подразделениям."""
        priority = {
            SourceChoices.SERVICE.value: 1,
            SourceChoices.ADMINISTRATION.value: 2,
            SourceChoices.DEPARTMENT.value: 3,
            SourceChoices.GROUP: 4,
        }
        conditions = []
        for source, value in priority.items():
            condition = When(
                division__source=source,
                then=Value(value),
            )
            conditions.append(condition)
        return self.annotate(
            priority=Case(
                *conditions,
                output_field=models.IntegerField(),
            )).order_by('priority')

    def retrieve(self):
        """Детальная информация о сотруднике."""
        return (
            self.prefetch_related('division')
            .annotate(division_id=models.F('division__id'))
            .annotate(start_at=models.F('employeedivision__start_at')))


class AbstractDivisionQuerySet(models.QuerySet):
    """Абстрактный QuerySet для подразделений."""

    def division_ids(self):
        """Получение всех id связанных подразделений."""
        raise NotImplementedError()


class ServiceQuerySet(AbstractDivisionQuerySet):
    """QuerySet служб."""

    def division_ids(self):
        """Получение всех id связанных подразделений."""
        values_list = [
            'division_id',
            'administrations__division_id',
            'administrations__departments__division_id',
            'administrations__departments__groups__division_id',
        ]
        return (
            self.values_list(*values_list)
            .prefetch_related('administrations')
            .prefetch_related('administrations__departments')
            .prefetch_related('administrations__departments__groups'))


class AdministrationQuerySet(AbstractDivisionQuerySet):
    """QuerySet управлений."""

    def division_ids(self):
        """Получение всех id связанных подразделений."""
        values_list = [
            'division_id',
            'departments__division_id',
            'departments__groups__division_id',
        ]
        return (
            self.values_list(*values_list)
            .prefetch_related('departments')
            .prefetch_related('administrations__departments__groups'))


class DepartmentQuerySet(AbstractDivisionQuerySet):
    """QuerySet отделов."""

    def division_ids(self):
        """Получение всех id связанных подразделений."""
        values_list = [
            'division_id',
            'groups__division_id',
        ]
        return (
            self.values_list(*values_list)
            .prefetch_related('groups'))


class GroupQuerySet(AbstractDivisionQuerySet):
    """QuerySet группы."""

    def division_ids(self):
        return self.values_list('division_id')
