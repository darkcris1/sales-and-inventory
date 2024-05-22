from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('item','payment_method', 'quantity', 'price', 'amount_received')
    list_display = ('item', 'slug', 'transaction_date', 'payment_method', 'quantity', 'price', 'total_value', 'amount_received', 'balance', 'profile')