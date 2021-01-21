from django.contrib import admin
from scripts.models import ScriptRecord

# Register your models here.

#admin.site.register(ScriptRecord)

@admin.register(ScriptRecord)
class ScriptAdmin(admin.ModelAdmin):
    fields = ['script_id', 'name', 'code', 'path', 'last_time_used']
    list_display = ['script_id', 'name', 'last_time_used']
    #list_filter = ['category']
    #search_fields = ['name', 'category', 'description']


