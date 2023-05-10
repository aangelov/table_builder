from rest_framework import serializers
from .models import Table


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = '__all__'


class TableSchemaSerializer(serializers.Serializer):
    schema = serializers.JSONField(required=True)


class TableDataSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)