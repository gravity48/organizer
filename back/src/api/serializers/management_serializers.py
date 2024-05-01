from rest_framework import serializers

from api import models


class ServiceSerializer(serializers.ModelSerializer):
    """Cериализатор службы."""

    division_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Service
        fields = [
            'id',
            'title',
            'division_id',
        ]


class AdministrationSerializer(serializers.ModelSerializer):
    """Сериализатор администрации."""

    service_id = serializers.SlugRelatedField(
        source='service',
        slug_field='id',
        queryset=models.Service.objects.all(),
    )

    division_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Administration
        fields = [
            'id',
            'title',
            'service_id',
            'division_id',
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор управления."""

    administration_id = serializers.SlugRelatedField(
        source='administration',
        slug_field='id',
        queryset=models.Administration.objects.all(),
    )

    division_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Department
        fields = [
            'id',
            'title',
            'administration_id',
            'division_id',
        ]


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор группы."""

    department_id = serializers.SlugRelatedField(
        source='department',
        slug_field='id',
        queryset=models.Department.objects.all(),
    )

    division_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Group
        fields = [
            'id',
            'title',
            'department_id',
            'division_id',
        ]
