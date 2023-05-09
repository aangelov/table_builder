from django.contrib import admin
from .models import Table


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


admin.site.register(Table, TableAdmin)
