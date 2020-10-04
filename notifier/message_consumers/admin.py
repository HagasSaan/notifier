from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import ConsumerModel, CustomConsumer


@admin.register(ConsumerModel)
class ConsumerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'object_type')

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(CustomConsumer)
class CustomConsumerAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
