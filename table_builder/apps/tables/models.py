from django.db import models
from django.db import connection
from django.db.utils import ProgrammingError
from rest_framework import serializers



class Table(models.Model):
    name = models.CharField(max_length=255, unique=True)
    schema = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_model(self):
        attrs = {
            'Meta': type('Meta', (), {'app_label': self._meta.app_label}),
            '__module__': __name__,
        }

        for field in self.schema:
            field_name = field['title']
            field_type = field['type']

            if field_type == 'string':
                # TODO: Is this length enough? Should we use TextField instead?
                # If length is limited validate on serializer level when row is added
                field_class = models.CharField(max_length=255)
            elif field_type == 'number':
                # TODO: Is decimal okay, should we use FloatField instead?
                # Limited to 2 decimal places?
                field_class = models.DecimalField(decimal_places=2, max_digits=10)
            elif field_type == 'boolean':
                field_class = models.BooleanField()

            attrs[field_name] = field_class

        model_class = type(self.name, (models.Model,), attrs)
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(model_class)
        except ProgrammingError:
            # table already exists
            # TODO: Handle update!
            pass

        return model_class

    @property
    def rows(self):
        model_class = self.create_model()
        rows = model_class.objects.all()
        return rows

    @property
    def serializer_class(self):
        """
        Create DRF serializer dynamically per model
        """
        attrs = {
            'Meta': type(
                'Meta',
                (),
                {
                    'model': self.create_model(),
                    'fields': '__all__'
                },
            ),
            '__module__': __name__,
        }
        serializer_class = type(
            self.name + 'Serializer',
            (serializers.ModelSerializer,),
            attrs
        )
        return serializer_class
