from django.db import connection

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from table_builder.apps.tables.models import Table
from table_builder.apps.tables import serializers


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = serializers.TableSerializer

    @swagger_auto_schema(
            request_body=serializers.TableSchemaSerializer,
            tags=['Update schema'],
    )
    @action(detail=True, methods=['put'])
    def update_schema(self, request, pk=None):
        table = self.get_object()

        serializer = serializers.TableSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table.schema = serializer.data.get('schema')
        table.save()

        # drop old table and create a new one
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(table.name)
        table.create_model()

        return Response({'success': 'Table schema updated'})

    @swagger_auto_schema(
            request_body=serializers.TableDataSerializer,
            tags=['Add rows to table'],
    )
    @action(detail=True, methods=['post'])
    def add_row(self, request, pk=None):
        table = self.get_object()

        serializer = serializers.TableDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model_class = table.create_model()
        row = model_class(**serializer.data.get('data'))
        row.save()

        return Response({'success': 'Row added'}, status=201)

    @swagger_auto_schema(
            tags=['Get table rows'],
    )
    @action(detail=True, methods=['get'])
    def get_rows(self, request, pk=None):
        table = self.get_object()
        serializer = table.serializer_class(table.rows, many=True)
        return Response(serializer.data)
