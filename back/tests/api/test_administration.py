import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAdministration:
    CREATE_LIST_URL = reverse('api:administration-list')

    def test_create_administration(
        self,
        test_client,
        faker,
        service_factory,
    ):
        """Проверка на создание управления."""
        service = service_factory()
        data = dict(
            title=faker.word(),
            service_id=service.id,
        )
        response = test_client.post(
            self.CREATE_LIST_URL,
            data=data
        )
        assert response.status_code == status.HTTP_201_CREATED
        administration = response.data
        assert isinstance(administration, dict)
        assert administration.get('title') == data['title']
        assert administration.get('service_id') == data['service_id']
        assert administration.get('division_id')
