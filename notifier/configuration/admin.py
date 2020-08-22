import structlog

from django.contrib import admin
from django.db.models import QuerySet
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from requests import Request

from .models import User, SkipKeyword, Configuration

logger = structlog.get_logger(__name__)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = (
        'last_login',
        'date_joined',
        'user_permissions',
        'groups',
        'is_staff',
        'is_superuser',
        'password',
        'email',
    )
    list_display = ('username', 'status', 'on_leave', 'is_working_time')
    list_filter = ('status', )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def is_working_time(self, obj: User) -> bool:
        return obj.is_working_time

    is_working_time.boolean = True


@admin.register(SkipKeyword)
class SkipKeywordAdmin(admin.ModelAdmin):
    list_display = ('word', )


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    actions = ('run_configurations', )

    def run_configurations(self, request: Request, queryset: QuerySet) -> None:
        for configuration in queryset:
            configuration.run()

    run_configurations.short_description = 'Run selected configurations'
