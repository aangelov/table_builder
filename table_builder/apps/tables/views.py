from django.db import connection

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Table
from .serializers import TableSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=['put'])
    def update_schema(self, request, pk=None):
        table = self.get_object()

        schema = request.data.get('schema')
        if not schema:
            return Response({'error': 'Missing schema'}, status=400)

        table.schema = schema
        table.save()

        # drop old table and create a new one
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(table.name)
        table.create_model()

        return Response({'success': 'Table schema updated'})

    @action(detail=True, methods=['post'])
    def add_row(self, request, pk=None):
        table = self.get_object()

        data = request.data.get('data')
        if not data:
            return Response({'error': 'Missing data'}, status=400)

        model_class = table.create_model()
        row = model_class(**data)
        row.save()

        return Response({'success': 'Row added'}, status=201)

    @action(detail=True, methods=['get'])
    def get_rows(self, request, pk=None):
        table = self.get_object()
        serializer = table.serializer_class(table.rows, many=True)
        return Response(serializer.data)
