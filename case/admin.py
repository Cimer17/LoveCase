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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'keys_count']
    list_editable = ['keys_count']

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'keys_count', 'is_single_use', 'activations_left']
    list_editable = ['keys_count', 'is_single_use', 'activations_left']
    list_display_links = ['code']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserItem, UserItemAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(PromoCode, PromoCodeAdmin)