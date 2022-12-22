from django.contrib import admin
from mdeditor.widgets import MDEditorWidget

from apps.models import *


class ClientChangelogAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


class WebChangelogAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(ScoreStore)
admin.site.register(ClientChangelog, ClientChangelogAdmin)
admin.site.register(WebChangelog, WebChangelogAdmin)
