from django.contrib import admin
from .models import *

class ItemInline(admin.TabularInline):
    model = Item.cases.through
    extra = 1

class CaseAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'chance')  # Определяем, какие поля будут отображаться в списке
    list_editable = ('quantity', 'chance')  # Определяем, какие поля будут доступны для редактирования прямо в списке
    search_fields = ('name',)  # Определяем поля, по которым можно будет выполнять поиск

class UserItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'conclusion', 'received_at')  # Поля для отображения в списке объектов
    list_filter = ('user', 'conclusion')  # Фильтры для быстрого поиска
    search_fields = ['user__username', 'item__name']  # Поля для поиска

admin.site.register(UserItem, UserItemAdmin)

admin.site.register(Case, CaseAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Game)