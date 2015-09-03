from django.contrib import admin

# Register your models here.
from . import models

class EntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'description', 'start', 'stop')
    list_filter = ('project',)
    search_fields = ('project', 'description',)


admin.site.register(models.Client)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Project)
