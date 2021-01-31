from django.contrib import admin
from scripts.models import ScriptRecord

@admin.register(ScriptRecord)
class ScriptAdmin(admin.ModelAdmin):
    fields = ['script_id', 'name', 'code', 'path', 'last_time_used']
    list_display = ['script_id', 'name', 'last_time_used']


