from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel

from . import managers
from .managers import AbstractDivisionQuerySet, SourceChoices


class Division(models.Model):
    """Подразделения."""

    id = models.UUIDField(
        default=uuid4,
        verbose_name=_('Уникальный идентификатор подразделения.'),
        primary_key=True,
        unique=True,
    )
    source = models.CharField(
        verbose_name=_('Подразделение'),
        max_length=15,
        choices=SourceChoices.choices,
    )

    @property
    def source_model(self):
        models = {
            SourceChoices.SERVICE.value: Service,
            SourceChoices.ADMINISTRATION.value: Administration,
            SourceChoices.DEPARTMENT.value: Department,
            SourceChoices.GROUP.value: Group,
        }
        model = models.get(self.source, None)
        if (
            model is None
            or not issubclass(model, BaseDivisionModel)
            or not isinstance(model.objects.get_queryset(), AbstractDivisionQuerySet)
        ):
            raise ValueError('Source model not available. Check database integrity.')
        return model

    class Meta:
        db_table = 'division'
        verbose_name = _('Подразделения')
        verbose_name_plural = _('Подразделение')


class BaseDivisionModel(BaseModel):
    """Базовый класс подразделений."""

    division = models.OneToOneField(
        Division,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        """Метод сохранения модели."""
        if self._state.adding:
            division = Division(source=self.__class__.__name__.upper())
            division.full_clean()
            division.save()
            self.division_id = division.id
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Service(BaseDivisionModel):
    """Службы."""

    title = models.CharField(
        verbose_name=_('Название службы'),
        max_length=100,
        unique=True,
    )

    objects = managers.ServiceQuerySet.as_manager()

    def __str__(self):
        return f'Service - {self.title}'

    class Meta:
        db_table = 'service'
        verbose_name = _('Службы')
        verbose_name_plural = _('Служба')


class Administration(BaseDivisionModel):
    """Управление."""

    title = models.CharField(
        verbose_name=_('Название управления'),
        max_length=100,
    )
    service = models.ForeignKey(
        'api.Service',
        verbose_name=_('Служба'),
        on_delete=models.CASCADE,
        related_name='administrations',
    )

    def __str__(self):
        return f'Administration - {self.title}'

    objects = managers.AdministrationQuerySet.as_manager()

    class Meta:
        db_table = 'administration'
        verbose_name = _('Управления')
        verbose_name_plural = _('Управление')


class Department(BaseDivisionModel):
    """Отдел."""

    title = models.CharField(
        verbose_name=_('Название отдела'),
        max_length=100,
    )

    administration = models.ForeignKey(
        'api.Administration',
        verbose_name=_('Управление'),
        on_delete=models.CASCADE,
        related_name='departments',
    )

    def __str__(self):
        return f'Department - {self.title}'

    objects = managers.DepartmentQuerySet.as_manager()

    class Meta:
        db_table = 'department'
        verbose_name = _('Отделы')
        verbose_name_plural = _('Отдел')


class Group(BaseDivisionModel):
    """Группы."""

    title = models.CharField(
        verbose_name=_('Название группы'),
        max_length=100,
    )

    department = models.ForeignKey(
        'api.Department',
        verbose_name=_('Отдел'),
        on_delete=models.CASCADE,
        related_name='groups',
    )

    def __str__(self):
        return f'Group - {self.title}'

    objects = managers.GroupQuerySet.as_manager()

    class Meta:
        db_table = 'group'
        verbose_name = _('Группы')
        verbose_name_plural = _('Группа')


class EmployeeDivision(models.Model):
    """Принадлежность сотрудника к группе."""

    employee = models.ForeignKey(
        'Employee',
        verbose_name=_('Сотрудник'),
        on_delete=models.CASCADE,
    )

    division = models.ForeignKey(
        'Division',
        verbose_name=_('Подразделение'),
        on_delete=models.CASCADE,
    )

    start_at = models.DateField(
        verbose_name=_('Дата начала работы'),
    )

    end_at = models.DateField(
        verbose_name=_('Дата окончания работы'),
        blank=True, null=True,
    )

    objects = managers.EmployeeDivisionQuerySet.as_manager()

    class Meta:
        db_table = 'employee_x_division'
        verbose_name = _('Личный состав подразделения.')
        verbose_name_plural = _('Подразделение сотрудника.')


class Employee(models.Model):
    """Сотрудники."""

    division = models.ManyToManyField(
        'Division',
        verbose_name=_('Подразделение'),
        related_name='employees',
        through='EmployeeDivision',
    )

    full_name = models.CharField(
        max_length=100,
        verbose_name=_('Полное имя'),
    )

    post = models.CharField(
        max_length=100,
        verbose_name=_('Должность'),
    )

    birthday = models.DateField(
        verbose_name=_('Дата рождения'),
    )

    photo = models.ImageField(
        verbose_name=_('Фото пользователя.'),
        upload_to='employee',
    )

    objects = managers.EmployeeQuerySet.as_manager()

    class Meta:
        db_table = 'employee'
        verbose_name = _('Сотрудники')
        verbose_name_plural = _('Сотрудник')
