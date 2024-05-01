from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from base import serializers as base_serializer
from api.models import Division, Employee, EmployeeDivision


class EmployeeListSerializer(serializers.ModelSerializer):
    """Сериализатор списка сотрудников."""

    division_title = serializers.CharField(read_only=True)
    division_type = serializers.CharField(read_only=True)
    start_at = serializers.DateField(read_only=True)
    photo = base_serializer.ImageField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'post',
            'birthday',
            'photo',
            'division_title',
            'division_type',
            'start_at',
        ]


class EmployeeDivisionSerializer(serializers.ModelSerializer):

    division_id = serializers.UUIDField()

    def validate_division_id(self, value):
        """Валидирует значение division_id."""
        if not Division.objects.filter(id=value).exists():
            raise ValidationError(_('Подразделение не найдено.'))
        return value

    class Meta:
        model = EmployeeDivision
        fields = (
            'division_id',
            'start_at',
        )


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания сотрудника."""

    id = serializers.IntegerField(read_only=True)
    division_id = serializers.SlugRelatedField(
        source='division__division',
        slug_field='id',
        queryset=Division.objects.all(),
    )
    start_at = serializers.DateField()
    photo = base_serializer.ImageField()

    @transaction.atomic()
    def save(self, **kwargs):
        employee_data = {
            'full_name': self.validated_data['full_name'],
            'post': self.validated_data['post'],
            'birthday': self.validated_data['birthday'],
            'photo': self.validated_data['photo'],
        }
        employee = Employee.objects.create(**employee_data)
        division_data = dict(
            employee_id=employee.id,
            division=self.validated_data['division__division'],
            start_at=self.validated_data['start_at'],
        )
        EmployeeDivision.objects.create(**division_data)
        self.validated_data['id'] = employee.id
        self.validated_data['photo'] = employee.photo
        return employee

    class Meta:
        model = Employee
        fields = (
            'id',
            'division',
            'post',
            'full_name',
            'birthday',
            'photo',
            'division_id',
            'start_at',
        )


class EmployeeRetrieveSerializer(serializers.ModelSerializer):

    division_id = serializers.UUIDField()

    start_at = serializers.DateField()
    photo = base_serializer.ImageField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'post',
            'full_name',
            'birthday',
            'photo',
            'division_id',
            'start_at',
        )


class EmployeeUpdateSerializer(serializers.ModelSerializer):

    division_id = serializers.UUIDField(required=False)
    start_at = serializers.DateField()
    photo = base_serializer.ImageField(required=False)

    def validate_division_id(self, value):
        """Валидирует значение division_id."""
        if not Division.objects.filter(id=value).exists():
            raise ValidationError(_('Подразделение не найдено.'))
        return value

    @transaction.atomic()
    def save(self, **kwargs):
        division_fields = dict(
            division_id=self.validated_data.get('division_id') or self.instance.division_id,
            start_at=self.validated_data['start_at'],
        )
        employee_data = dict(
            full_name=self.validated_data['full_name'],
            post=self.validated_data['post'],
            birthday=self.validated_data['birthday'],
        )
        if self.validated_data.get('photo'):
            employee_data['photo'] = self.validated_data['photo']
        for attr, value in employee_data.items():
            setattr(self.instance, attr, value)
        self.instance.save()
        EmployeeDivision.objects.filter(employee_id=self.instance.id).update(**division_fields)
        self.validated_data['photo'] = self.instance.photo
        return self.validated_data

    class Meta:
        model = Employee
        fields = (
            'post',
            'full_name',
            'birthday',
            'photo',
            'division_id',
            'start_at',
        )
