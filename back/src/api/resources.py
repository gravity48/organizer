from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from . import serializers


GET_SUCCESS_MANAGEMENT_TREE_200 = {
    200: OpenApiResponse(
        description='Успешное получение структуры подразделений пользователем.',
        response=serializers.ManagementResponseSerializer(many=True),
        examples=[
            OpenApiExample(
                'Пример ответа',
                value={
                    'id': 1,
                    'title': 'Заголовок узла дерева',
                    'source': 'root',
                    'children': [],
                },
            ),
        ],
    ),
}

NODE_NOT_FOUND_MANAGEMENT_TREE_404 = {
    404: OpenApiResponse(
        description='Переданный узел не найден.',
        examples=[
            OpenApiExample(
                'Узел не найден',
                value={
                    'detail': 'Указанный узел не существует.',
                },
            ),
        ],
    ),
}

MANAGEMENT_TREE_RESOURCES = {
    **GET_SUCCESS_MANAGEMENT_TREE_200,
    **NODE_NOT_FOUND_MANAGEMENT_TREE_404,
}


GET_SUCCESS_LIST_EMPLOYEES = {
    200: OpenApiResponse(
        description='Успешное получение сотрудников',
        response=serializers.EmployeeListSerializer(many=True),
    ),
}


GET_SUCCESS_EMPLOYEE_STATS = {
    200: OpenApiResponse(
        description='Успешное получение статистики подразделения.',
        response=serializers.EmployeeStatSerializer,
        examples=[
            OpenApiExample(
                'Пример ответа с сотрудниками',
                value={
                    'employee_count': 1,
                    'employee_avg_year': '30 лет',
                    'employee_avg_exp': '5 лет 2 месяца 3 дня',
                },
            ),
            OpenApiExample(
                'Пример ответа без сотрудников',
                value={
                    'employee_count': 0,
                    'employee_avg_year': 'null',
                    'employee_avg_exp': 'null',
                },
            ),
        ],
    ),
}
