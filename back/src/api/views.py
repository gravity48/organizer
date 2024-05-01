from django.http import Http404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import filters, models, resources, serializers
from .mixins import DivisionActionMixin
from .tree_service import service_tree
from .tree_service.base import TreeFactoryNodeNotFoundError


@extend_schema(
    tags=['Структура подразделений'],
    methods=['GET'],
    description='Получение структуры подразделений.',
    parameters=[serializers.ManagementRequestSerializer],
    responses=resources.MANAGEMENT_TREE_RESOURCES,
)
@api_view(['GET'])
def management_struct_view(request):
    """Получение дерева подразделений."""
    serializer = serializers.ManagementRequestSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    try:
        tree_data = service_tree.generate_tree(**serializer.validated_data)
    except TreeFactoryNodeNotFoundError:
        raise Http404(_('Указанный узел не существует.'))
    serializer = serializers.ManagementResponseSerializer(tree_data)
    return Response(serializer.data)


@extend_schema(
    tags=['Служба'],
)
class ServiceView(DivisionActionMixin, ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get_division_ids_qs(self, pk: int):
        return (
            models.Service
            .objects.filter(pk=pk)
            .division_ids())


@extend_schema(
    tags=['Администрация'],
)
class AdministrationView(DivisionActionMixin, ModelViewSet):
    queryset = models.Administration.objects.all()
    serializer_class = serializers.AdministrationSerializer
    filterset_fields = ['service_id']

    def get_division_ids_qs(self, pk: int):
        return (
            models.Administration
            .objects.filter(pk=pk)
            .division_ids())

    @extend_schema(
        parameters=[
            OpenApiParameter('service_id', OpenApiTypes.INT),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=['Отдел'],
)
class DepartmentView(DivisionActionMixin, ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    filterset_fields = ['administration_id']

    @extend_schema(
        parameters=[
            OpenApiParameter('administration_id', OpenApiTypes.INT),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_division_ids_qs(self, pk: int):
        return (
            models.Department
            .objects.filter(pk=pk)
            .division_ids())


@extend_schema(
    tags=['Группа'],
)
class GroupView(DivisionActionMixin, ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    filterset_fields = ['department_id']

    @extend_schema(
        parameters=[
            OpenApiParameter('department_id', OpenApiTypes.INT),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_division_ids_qs(self, pk: int):
        return (
            models.Group
            .objects.filter(pk=pk)
            .division_ids())


@extend_schema(
    tags=['Сотрудники'],
)
class EmployeeCreateListView(generics.ListCreateAPIView):
    filter_backends = [filters.EmployeeDivisionFilter]
    http_method_names = ['post', 'get']
    serializers = {
        'POST': serializers.EmployeeCreateSerializer,
        'GET': serializers.EmployeeListSerializer,
    }

    @extend_schema(
        parameters=[
            OpenApiParameter('division_id', OpenApiTypes.UUID),
        ],
        responses=resources.GET_SUCCESS_LIST_EMPLOYEES,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        method = self.request.method
        serializer = self.serializers.get(method, None)
        return serializer

    def get_queryset(self):
        return (
            models.Employee
            .objects
            .prefetch_all()
            .division_info()
            .order_by_source())


@extend_schema(
    tags=['Сотрудники'],
)
class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'delete']
    serializers = {
        'GET': serializers.EmployeeRetrieveSerializer,
        'PUT': serializers.EmployeeUpdateSerializer,
    }

    queryset = (
        models.Employee
        .objects
        .retrieve())

    def get_serializer_class(self):
        method = self.request.method
        serializer = self.serializers.get(method, None)
        return serializer
