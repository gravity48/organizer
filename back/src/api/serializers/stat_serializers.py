from rest_framework import serializers

from base.utils import days_to_ymd, plural_russian_date


class EmployeeAvgYearField(serializers.IntegerField):

    def to_representation(self, value) -> str:
        return plural_russian_date(
            year=value,
        )


class EmployeeAvgExpField(serializers.IntegerField):

    def to_representation(self, value) -> str:
        year, month, days = days_to_ymd(value)
        return plural_russian_date(
            year=year,
            month=month,
            days=days,
        )


class EmployeeStatSerializer(serializers.Serializer):
    """Сериалайзер статистики подразделения."""

    employee_count = serializers.IntegerField()
    employee_avg_year = EmployeeAvgYearField()
    employee_avg_exp = EmployeeAvgExpField()
