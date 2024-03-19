from django.contrib import admin
from .models import PromoCode

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'keys_count', 'is_single_use', 'activations_left']
    list_editable = ['keys_count', 'is_single_use', 'activations_left']
    list_display_links = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)