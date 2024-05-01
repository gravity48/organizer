import datetime

import pytest
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class TestService:

    BASE_URL = reverse('api:service-list')

    def test_service_stats(
        self,
        test_client,
        service_factory,
        administration_factory,
        department_factory,
        working_employee,
    ):
        """Проверка на получение статистики по службе."""
        service = service_factory()
        administration = administration_factory(service_id=service.id)
        administration_factory(service_id=service.id)
        twenty_years_old = datetime.date.today() - relativedelta(years=20)
        forty_years_old = datetime.date.today() - relativedelta(years=40)
        working_employee(
            division_id=service.division_id,
            birthday=twenty_years_old,
        )
        working_employee(
            division_id=administration.division_id,
            birthday=forty_years_old,
        )
        url = f'{self.BASE_URL}{service.id}/stat/'
        response = test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        employee_stat = response.data
        assert isinstance(employee_stat, dict)
        assert employee_stat.get('employee_count') == 2
        assert employee_stat.get('employee_avg_year') == '30 лет'
        assert employee_stat.get('employee_avg_exp')

    def test_success_no_employee_service_stat(
        self,
        test_client,
        service_factory,
    ):
        """Проверка на получение статистики подразделения без сотрудников."""
        service = service_factory()
        url = f'{self.BASE_URL}{service.id}/stat/'
        response = test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        employee_stat = response.data
        assert isinstance(employee_stat, dict)
        assert employee_stat.get('employee_count') == 0
        assert employee_stat.get('employee_avg_year') is None
        assert employee_stat.get('employee_avg_exp') is None
