from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    list_display = (
        'username',
        'slug',
        'first_name',
        'last_name',
        'date_of_birth',
    )

    list_display_links = ('username', 'slug')
    prepopulated_fields = {'slug': ('username',)}

