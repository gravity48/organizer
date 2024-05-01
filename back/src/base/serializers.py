from rest_framework import serializers


class ImageField(serializers.ImageField):

    def to_representation(self, value):
        """Отображение url."""
        if not value:
            return None
        return value.url
