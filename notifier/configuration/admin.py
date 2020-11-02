import structlog
from django.conf import settings

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.urls.resolvers import RoutePattern
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from requests import Request

from .forms import ScheduleConfigurationForm
from .models import User, Configuration, MessageFilterModel
from .tasks import run_configuration
from .use_cases import ScheduleConfigurationUseCase

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


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    actions = ('run_configurations', )

    change_list_template = 'admin/configuration_change_list.html'

    def run_configurations(self, request: Request, queryset: list[Configuration]) -> None:
        for configuration in queryset:
            if settings.SYNC_MODE:
                configuration.run()
            else:
                run_configuration.delay(configuration.id)

    run_configurations.short_description = 'Run selected configurations'

    def get_urls(self) -> list[RoutePattern]:
        urls = super().get_urls()
        my_urls = [
            path(
                'schedule_configuration/',
                self.admin_site.admin_view(self.schedule_configuration),
                name='schedule_configuration',
            ),
        ]
        return my_urls + urls

    def schedule_configuration(self, request: WSGIRequest) -> TemplateResponse:
        context = dict(self.admin_site.each_context(request))

        if request.method != 'POST':
            form = ScheduleConfigurationForm()
            context['form'] = form
            return TemplateResponse(
                request,
                'admin/schedule_configuration.html',
                context,
            )

        form = ScheduleConfigurationForm(request.POST, request.FILES)
        if not form.is_valid():
            return TemplateResponse(
                request,
                'admin/schedule_configuration.html',
                context,
            )

        ScheduleConfigurationUseCase(**form.cleaned_data).execute()
        url_name = 'admin:configuration_configuration_changelist'
        return redirect(reverse(url_name))


@admin.register(MessageFilterModel)
class MessageFilterModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
