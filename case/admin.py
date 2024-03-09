from django.contrib import admin
from case.models import *


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1  # Количество пустых форм для добавления

class CaseAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(Case, CaseAdmin)