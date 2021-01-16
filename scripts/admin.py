from django.contrib import admin
from scripts.models import ScriptRecord

# Register your models here.

#admin.site.register(ScriptRecord)

@admin.register(ScriptRecord)
class ScriptAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'description', 'code']
    list_display = ['name', 'category', 'description']
    list_filter = ['category']
    search_fields = ['name', 'category', 'description']


