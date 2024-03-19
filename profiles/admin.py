from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'keys_count']
    list_editable = ['keys_count']


admin.site.register(UserProfile, UserProfileAdmin)