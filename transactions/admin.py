from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'begin_inventory', 'damage', 'delivery', 'sales', 'withdrawal', 'ending_inventory', 'remarks', 'transaction_date')

    search_fields = ['item__name']