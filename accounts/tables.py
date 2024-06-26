# tutorial/tables.py
import django_tables2 as tables
from .models import Profile
from django.shortcuts import render

class ProfileTable(tables.Table):
    class Meta:
        model = Profile
        template_name = "django_tables2/semantic.html"
        fields = ('date','contact_number','item','price_per_item', 'total')
        order_by_field = 'sort'