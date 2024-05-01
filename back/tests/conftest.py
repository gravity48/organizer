import pytest
from api import models as api_models
from rest_framework.test import APIClient


@pytest.fixture()
def test_client():
    return APIClient()


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['ru_RU']


@pytest.fixture()
def service_factory(faker):
    def _create_item(**kwargs):
        params = dict(
            title=faker.unique.word(),
        )
        params.update(kwargs)
        return api_models.Service.objects.create(**params)
    return _create_item


@pytest.fixture()
def administration_factory(
    faker,
    service_factory,
):
    def _create_item(service_id=None, **kwargs):
        if not service_id:
            service = service_factory()
            service_id = service.id
        params = dict(
            title=faker.unique.word(),
            service_id=service_id,
        )
        params.update(kwargs)
        return api_models.Administration.objects.create(**params)
    return _create_item


@pytest.fixture()
def department_factory(
    faker,
    administration_factory,
):
    def _create_item(administration_id=None, **kwargs):
        if not administration_id:
            administration = administration_factory()
            administration_id = administration.id
        params = dict(
            title=faker.unique.word(),
            administration_id=administration_id,
        )
        params.update(kwargs)
        return api_models.Department.objects.create(**params)
    return _create_item


@pytest.fixture()
def group_factory(
    faker,
    department_factory,
):
    def _create_item(department_id=None, **kwargs):
        if not department_id:
            department = department_factory()
            department_id = department.id
        params = dict(
            title=faker.unique.word(),
            department_id=department_id,
        )
        params.update(kwargs)
        return api_models.Group.objects.create(**params)
    return _create_item


@pytest.fixture()
def employee_division(
    faker,
):

    def _create_item(division_id: int, employee_id: int, **kwargs):
        params = dict(
            division_id=division_id,
            employee_id=employee_id,
            start_at=faker.date_between('-20y'),
            end_at=None,
        )
        params.update(kwargs)
        return api_models.EmployeeDivision.objects.create(**params)
    return _create_item


@pytest.fixture()
def working_employee(
    faker,
    employee_division,
):

    def _create_item(division_id: int, **kwargs):
        params = dict(
            full_name=faker.name(),
            post=faker.word(),
            birthday=faker.date_of_birth(
                minimum_age=18,
                maximum_age=50,
            ),
        )
        params.update(kwargs)
        employee = api_models.Employee.objects.create(**params)
        employee_division(division_id, employee.id)
        return employee

    return _create_item
