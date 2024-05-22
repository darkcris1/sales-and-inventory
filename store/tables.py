# tutorial/tables.py
import django_tables2 as tables
from .models import Item
from django.shortcuts import render

class ItemTable(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/semantic.html"
        fields = ('id', 'name','category', 'selling_price', 'expiring_date')
        order_by_field = 'sort'