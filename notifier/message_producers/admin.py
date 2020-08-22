from django.contrib import admin

from .models import ProducerModel
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(ProducerModel)
class ProducerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'object_type')

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
