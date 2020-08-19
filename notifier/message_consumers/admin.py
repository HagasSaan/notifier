from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import ConsumerModel


@admin.register(ConsumerModel)
class ConsumerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
