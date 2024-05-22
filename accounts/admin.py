from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Profile)
class StatisticDiff(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'email', 'role', 'status')
