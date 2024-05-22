from django.contrib import admin
from .models import Category, Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ('name', 'category','selling_price', )
    list_display = ('id', 'name','category', 'selling_price', )
    search_fields = ['id', 'name']

admin.site.register(Category)