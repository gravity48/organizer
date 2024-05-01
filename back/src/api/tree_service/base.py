from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional

from django.db.models import Case, CharField, Prefetch, QuerySet, Value

from api.models import BaseModel


class TreeFactoryBaseError(Exception):
    """Базовая ошибка генерации дерева."""


class TreeFactoryLayerNotFoundError(TreeFactoryBaseError):
    """Не найден соответствующий слой."""


class TreeFactoryNodeNotFoundError(TreeFactoryBaseError):
    """Не найден узел дерева."""


@dataclass
class Node:
    """Узел дерева."""

    id: int
    title: str
    source: str
    children: list


class Layer:
    next: Optional['Layer'] = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Layer - {self.name}'


class RootLayer(Layer):
    """Корневой слой дерева."""

    next: Optional['ModelLayer'] = None


class ModelLayer(Layer):
    """Слой моделей."""

    model: BaseModel = None
    related_name = None

    @property
    def query(self):
        """Запрос для получения вложенных объектов."""
        return self.model.objects.annotate(
            source=Case(
                default=Value(self.name),
                output_field=CharField(),
            ),
        ).all()


def _queryset_generator(layer, layer_qs, indent):
    """Генерирует qs для построения дерева."""
    if layer.next is None or indent == 0:
        return layer.query
    if indent:
        indent -= 1
    return layer_qs.prefetch_related(
        Prefetch(
            layer.next.related_name,
            queryset=_queryset_generator(layer.next, layer.next.query, indent),
            to_attr='children',
        ),
    )


class TreeFactory:
    layers: OrderedDict[str, ModelLayer] = None

    def __init__(self, title: str):
        self.layers = OrderedDict()
        self.title = title
        self.root_layer = RootLayer(title)

    def add_layer(self, layer: ModelLayer):
        """Добавляет слой и формирует связанный список."""
        if self.layers:
            prev_key: str = next(reversed(self.layers))
            prev_layer = self.layers[prev_key]
        else:
            prev_layer = self.root_layer
        self.layers[layer.name] = layer
        prev_layer.next = layer

    def get_layer_by_name(self, layer_name) -> ModelLayer | RootLayer:
        """Получает слой по его имени."""
        if layer_name == 'root':
            return self.root_layer
        try:
            return self.layers[layer_name]
        except KeyError as exp:
            raise TreeFactoryLayerNotFoundError from exp

    @staticmethod
    def _get_tree_data_queryset(
        layer: ModelLayer,
        layer_qs: QuerySet,
        indent: Optional[int] = None,
    ) -> QuerySet:
        """Формирует queryset для получения данных дерева."""
        try:
            return _queryset_generator(layer, layer_qs, indent)
        except Exception as exp:
            raise TreeFactoryBaseError from exp

    def _generate_tree_by_root_layer(
        self,
        indent: Optional[int],
    ):
        """Генератор дерева для root слоя."""
        layer = self.root_layer.next
        layer_qs = layer.query
        if indent == 0:
            tree_data = []
        else:
            indent = indent and indent - 1
            tree_data_qs = self._get_tree_data_queryset(
                layer,
                layer_qs,
                indent,
            )
            tree_data = list(tree_data_qs)
        node = Node(
            title=self.title,
            id=1,
            source='root',
            children=tree_data,
        )
        return node

    def _generate_tree_by_model_layer(
        self,
        layer: ModelLayer,
        source_id: int,
        indent: Optional[int] = None,
    ):
        """Формирует дерево для слоя моделей."""
        layer_qs = layer.query
        layer_qs = layer_qs.filter(pk=source_id)
        tree_data_qs: QuerySet = self._get_tree_data_queryset(
            layer,
            layer_qs,
            indent,
        )
        tree_data = tree_data_qs.first()
        if not tree_data:
            raise TreeFactoryNodeNotFoundError
        return tree_data

    def generate_tree(
        self,
        source: str,
        source_id: int = 1,
        indent: Optional[int] = None,
    ):
        """Генерирует дерево."""
        layer = self.get_layer_by_name(layer_name=source)
        if isinstance(layer, RootLayer):
            return self._generate_tree_by_root_layer(indent)
        return self._generate_tree_by_model_layer(
            layer,
            source_id,
            indent,
        )
