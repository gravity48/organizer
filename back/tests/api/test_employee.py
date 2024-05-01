import datetime

import pytest
from api import models
from django.conf import settings
from django.urls import reverse
from rest_framework import status


EMPLOYEE_PHOTO_PATH = settings.TEST_STATIC_FILES_FIR / 'person.png'


@pytest.mark.django_db
class TestEmployee:
    BASE_URL = reverse('api:employee_list_create')

    def test_success_list_employee(
        self,
        test_client,
        service_factory,
        administration_factory,
        department_factory,
        working_employee,
    ):
        """Проверка на получение списка сотрудников."""
        filter_division = service_factory()
        filter_subdivision = administration_factory(service_id=filter_division.id)
        first_employee = working_employee(filter_division.division_id)
        second_employee_2 = working_employee(filter_subdivision.division_id)
        filter_employees = [first_employee, second_employee_2]
        no_filter_division = service_factory()
        no_filter_employee = working_employee(no_filter_division.division_id)
        data = dict(
            division_id=filter_division.division_id,
        )
        response = test_client.get(
            self.BASE_URL,
            data=data,
        )
        assert response.status_code == status.HTTP_200_OK
        employees = response.data
        assert isinstance(employees, list)
        assert len(employees) == len(filter_employees)
        employees_ids = list(map(lambda employee: employee['id'], employees))
        for filter_employee in filter_employees:
            assert filter_employee.id in employees_ids
        first_result_employee = employees[0]
        assert first_result_employee['id'] == first_employee.id
        assert first_result_employee['division_title'] == filter_division.title
        assert first_result_employee['division_type'] == 'SERVICE'
        assert no_filter_employee not in employees_ids

    def test_success_create_employee(
        self,
        test_client,
        faker,
        service_factory,
        administration_factory,
        working_employee,
    ):
        """Проверка на успешное создание сотрудника."""
        division = service_factory()
        data = dict(
            division_id=division.division_id,
            start_at=faker.date_between('-20y'),
            full_name=faker.name(),
            post=faker.word(),
            birthday=faker.date_of_birth(
                minimum_age=18,
                maximum_age=50,
            ),
        )
        with EMPLOYEE_PHOTO_PATH.open('rb') as file:
            data['photo'] = file
            response = test_client.post(
                self.BASE_URL,
                data,
                format='multipart',
            )
        assert response.status_code == status.HTTP_201_CREATED
        db_employee = (
            models.Employee.objects
            .prefetch_related('division')
            .filter(full_name=data['full_name'])
            .first())
        assert db_employee is not None
        employee = response.data
        assert isinstance(employee, dict)
        assert db_employee.id == employee['id']
        assert db_employee.full_name == employee['full_name']
        assert db_employee.post == employee['post']
        assert db_employee.birthday.strftime('%d.%m.%Y') == employee['birthday']
        db_divisions = db_employee.division.all()
        assert len(db_divisions) == 1
        db_division = db_divisions[0]
        assert db_division.id == employee.get('division_id')
        assert employee.get('photo')

    def test_success_retrieve_employee(
        self,
        test_client,
        group_factory,
        working_employee,
    ):
        """Проверка на получение детальной информации о пользователе."""
        group = group_factory()
        db_employee = working_employee(group.division_id)
        response = test_client.get(f'{self.BASE_URL}{db_employee.id}/')
        assert response.status_code == status.HTTP_200_OK
        employee = response.data
        assert isinstance(employee, dict)
        assert employee.get('post') == db_employee.post
        assert employee.get('full_name') == db_employee.full_name

    def test_success_update_employee_without_photo(
        self,
        test_client,
        service_factory,
        administration_factory,
        working_employee,
        faker,
    ):
        """Проверка на обновление пользователя."""
        service = service_factory()
        new_division = administration_factory()
        db_employee = working_employee(division_id=service.division_id)
        update_data = dict(
            full_name='new_full_name',
            post='new_post',
            birthday=faker.date_of_birth(
                minimum_age=51,
                maximum_age=52,
            ),
            start_at=datetime.date.today(),
            division_id=new_division.division_id)
        response = test_client.put(
            f'{self.BASE_URL}{db_employee.id}/',
            update_data,
            format='multipart',
        )
        assert response.status_code == 200
        updated_employee = response.data
        assert isinstance(updated_employee, dict)
        db_employee = models.Employee.objects.get(pk=db_employee.id)
        fields = {'full_name', 'post', 'birthday'}
        for field in fields:
            assert getattr(db_employee, field) == update_data[field]
        division_info = (
            models.EmployeeDivision
            .objects.filter(employee_id=db_employee.id)
            .first())
        assert division_info
        division_info_fields = {'division_id', 'start_at'}
        for field in division_info_fields:
            assert getattr(division_info, field) == update_data[field]

    def test_success_update_employee_with_photo(
        self,
        test_client,
        service_factory,
        administration_factory,
        working_employee,
        faker,
    ):
        """Проверка на обновление пользователя."""
        service = service_factory()
        new_division = administration_factory()
        db_employee = working_employee(division_id=service.division_id)
        update_data = dict(
            full_name='new_full_name',
            post='new_post',
            birthday=faker.date_of_birth(
                minimum_age=51,
                maximum_age=52,
            ),
            start_at=datetime.date.today(),
            division_id=new_division.division_id)
        with EMPLOYEE_PHOTO_PATH.open('rb') as file:
            update_data['photo'] = file
            response = test_client.put(
                f'{self.BASE_URL}{db_employee.id}/',
                update_data,
                format='multipart',
            )
        assert response.status_code == 200
        updated_employee = response.data
        assert isinstance(updated_employee, dict)
        db_employee = models.Employee.objects.get(pk=db_employee.id)
        fields = {'full_name', 'post', 'birthday'}
        for field in fields:
            assert getattr(db_employee, field) == update_data[field]
        assert db_employee.photo
        division_info = (
            models.EmployeeDivision
            .objects.filter(employee_id=db_employee.id)
            .first())
        assert division_info
        division_info_fields = {'division_id', 'start_at'}
        for field in division_info_fields:
            assert getattr(division_info, field) == update_data[field]

    def test_success_delete_employee(
        self,
        test_client,
        service_factory,
        working_employee,
    ):
        """Проверка на удаление пользователя."""
        service = service_factory()
        employee = working_employee(service.division_id)
        response = test_client.delete(f'{self.BASE_URL}{employee.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        db_employee = (
            models.Employee.objects
            .filter(id=employee.id)
            .first())
        assert db_employee is None
        db_employee_division = (
            models.EmployeeDivision
            .objects
            .filter(employee_id=employee.id)
            .first())
        assert db_employee_division is None
