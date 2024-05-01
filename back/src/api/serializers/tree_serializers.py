from rest_framework import serializers

from api.tree_service import SourcesEnum


class ManagementRequestSerializer(serializers.Serializer):
    """Сериализатор запроса на построение дерева управления."""

    source = serializers.ChoiceField(
        choices=SourcesEnum.values(),
    )
    source_id = serializers.IntegerField(min_value=1)
    indent = serializers.IntegerField(min_value=0, required=False)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ManagementResponseSerializer(serializers.Serializer):
    """Сериализатор ответа построения дерева управления."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    source = serializers.CharField()
    division_id = serializers.UUIDField(required=False)
    children = RecursiveSerializer(many=True, read_only=True)
