import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestManagementStruct:
    BASE_URL = reverse('api:management_struct_view')

    def test_success_tree_by_root_layer(
        self,
        test_client,
        service_factory,
        administration_factory,
        department_factory,
    ):
        """Проверка на получение дерева c корневого элемента."""
        service = service_factory()
        administration = administration_factory(service_id=service.id)
        administration_factory(service_id=service.id)
        administration_factory()
        department_factory(administration_id=administration.id)
        data = dict(
            source='root',
            source_id=1,
            indent=1,
        )
        response = test_client.get(
            self.BASE_URL,
            data=data,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert isinstance(data, dict)
        assert data.get('id') == 1
        assert data.get('title') == 'Подразделения'
        assert data.get('source') == 'root'

    def test_success_tree_by_model_layer(
        self,
        test_client,
        service_factory,
        administration_factory,
        department_factory,
    ):
        """Проверка на получение дерева управления не c корневого элемента."""
        service = service_factory()
        service_administration = administration_factory(service_id=service.id)
        service_administration2 = administration_factory(service_id=service.id)
        no_service_administration2 = administration_factory()
        department_factory(administration_id=service_administration.id)
        data = dict(
            source='service',
            source_id=service.id,
            indent=1,
        )
        response = test_client.get(
            self.BASE_URL,
            data=data,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert isinstance(data, dict)
        assert data.get('id') == service.id
        assert data.get('title') == service.title
        assert data.get('source') == 'service'
        assert data.get('division_id')
        assert isinstance(data.get('children'), list)
        children = data.get('children')
        assert len(children) == 2
        children_ids = list(map(lambda item: item['id'], children))
        assert service_administration.id in children_ids
        assert service_administration2.id in children_ids
        assert no_service_administration2 not in children_ids

    def test_node_not_found(
        self,
        test_client,
        administration_factory,
        department_factory,
    ):
        """Проверка на то что указанный узел не найден."""
        administration = administration_factory()
        department_factory(administration_id=administration.id)
        not_found_id = 2
        data = dict(
            source='department',
            source_id=not_found_id,
        )
        response = test_client.get(
            self.BASE_URL,
            data=data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert isinstance(data, dict)
        assert data.get('detail') == 'Указанный узел не существует.'
