from django.contrib import admin
from .models import  Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'barcode', 'barcode' )
    search_fields = ['id', 'name']