# tutorial/tables.py
import django_tables2 as tables
from .models import Sale
from django.shortcuts import render

class SaleTable(tables.Table):
    class Meta:
        model = Sale
        template_name = "django_tables2/semantic.html"
        fields = ('item', 'transaction_date', 'initial_stock' ,'damage', 'withdrawal', 'delivery', 'sales','', 'remarks',  'profile')
        order_by_field = 'sort'